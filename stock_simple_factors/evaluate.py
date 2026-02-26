'''
Author: Qimin Ma
Date: 2026-02-24 22:18:23
LastEditTime: 2026-02-25 22:21:42
FilePath: /Dataset/stock_simple_factors/evaluate.py
Description:    
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from base import TushareBigConstantLoader
import logging
from datetime import datetime
import pandas as pd
import tushare as ts
from reader import LoadDaily, LoadFundamental
import duckdb
from smart_data_loader.fundamental.fundamental import FundamentalPreprocessor


class Evaluate(TushareBigConstantLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        self.start = start
        self.end = end
        super().__init__(logger, db_name='stock_classic_factors', table_name='evaluate')

    def _run_func_onetime(self) -> pd.DataFrame:
        LoadDaily(
            db_name='raw_tushare',
            table_name="stock_daily",
            start=self.start,
            end=self.end,
            columns=['InnerCode','TradingDay','pe_ttm','pb','ps_ttm','total_mv'],
            duckdb_variable='raw'
        )

        LoadFundamental(
            db_name="raw_tushare",
            table_name="cashflow",
            start=self.start,
            end=self.end,
            columns=['InnerCode','f_ann_date','n_cashflow_act','n_incr_cash_cash_equ','free_cashflow'],
            duckdb_variable='cashflow'
        )

        LoadFundamental(
            db_name="raw_tushare",
            table_name="fina_indicator",
            start=self.start,
            end=self.end,
            columns=['InnerCode','end_date','netprofit_yoy','ebitda'],
            duckdb_variable='fina_indicator'

        )

        LoadFundamental(
            db_name="raw_tushare",
            table_name="balance",
            start=self.start,
            end=self.end,
            columns=['InnerCode','f_ann_date','st_borr','lt_borr','bond_payable','money_cap'],
            duckdb_variable='balance'
        )

        LoadDaily(
            db_name='raw_tushare',
            table_name="stock_daily",
            start=self.start,
            end=self.end,
            columns=['InnerCode','TradingDay'],
            duckdb_variable='all_stocks'
        )

        cashflow = FundamentalPreprocessor(
            logger=self.logger,
            fundamental_table='cashflow',
            all_stock_table='all_stocks',
        )
        cashflow.ffill_na()
        cashflow.backward_fill_na()
        cashflow.cal_ttm(["n_cashflow_act", "n_incr_cash_cash_equ", "free_cashflow"], windows=252)
        duckdb.register('cashflow', cashflow.merge_df)

        fina_indicator = FundamentalPreprocessor(
            logger=self.logger,
            fundamental_table='fina_indicator',
            all_stock_table='all_stocks',
            merging_date_type='end_date',
        )
        fina_indicator.ffill_na()
        fina_indicator.backward_fill_na()
        duckdb.register('fina_indicator', fina_indicator.merge_df)

        balance = FundamentalPreprocessor(
            logger=self.logger,
            fundamental_table='balance',
            all_stock_table='all_stocks',
        )
        balance.ffill_na()
        balance.backward_fill_na()
        balance.cal_ttm(["st_borr", "lt_borr", "bond_payable", "money_cap"], windows=252)
        duckdb.register('balance', balance.merge_df)


        duckdb.sql(f"""
        create or replace table evaluate as
        select a.InnerCode,
               a.TradingDay,
               1/a.pe_ttm as ep,
               1/a.pb as bp,
               1/a.ps_ttm as sp,
               b.n_incr_cash_cash_equ_ttm / a.total_mv as ncfp,
               b.n_cashflow_act_ttm / a.total_mv as ocfp,
               b.free_cashflow_ttm / a.total_mv as fcfp,
               a.pe_ttm / c.netprofit_yoy as peg,
               (a.total_mv + d.st_borr_ttm + d.lt_borr_ttm + d.bond_payable_ttm - d.money_cap_ttm) / c.ebitda as ev2ebitda
               from raw a
               left join cashflow b
               on a.InnerCode = b.InnerCode and a.TradingDay = b.TradingDay
               left join fina_indicator c
               on a.InnerCode = c.InnerCode and a.TradingDay = c.TradingDay
               left join balance d
               on a.InnerCode = d.InnerCode and a.TradingDay = d.TradingDay
               """)

        return 'evaluate'