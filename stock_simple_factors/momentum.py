'''
Author: Qimin Ma
Date: 2026-02-21 16:39:01
LastEditTime: 2026-02-24 21:53:04
FilePath: /Dataset/stock_simple_factors/momentum.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from dataclasses import dataclass

from pandas.core.strings.accessor import str_extractall
from base import TushareDailyLoader, TushareConstantLoader, TushareBigConstantLoader
import logging
from datetime import datetime
import pandas as pd
import tushare as ts
import os
import numpy as np
import duckdb
from sklearn.linear_model import LinearRegression
from reader import LoadDaily, LoadConstant
from smart_data_loader.logger import get_logger


class Momentum(TushareBigConstantLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d'),
                windows:list[int]=[5, 21, 63, 126, 252],
                turnover_type="turnover_rate") -> None:
        self.windows = windows
        self.turnover_col = turnover_type
        self.start = start
        self.end = end
        super().__init__(logger, db_name='stock_classic_factors', \
            table_name='momentum')

    def _load_data(self):
        LoadDaily(
            db_name='raw_tushare',
            table_name='stock_daily',
            start =self.start,
            end = self.end,
            columns=['InnerCode', 'TradingDay', 'close', self.turnover_col, 'pct_chg'],
            condition = 'order by InnerCode, TradingDay',
            duckdb_variable='stock_daily'
        )

        self.logger.info(f'Finish loading data for date: {self.start} to {self.end}')

    def _calculate_momentum_return(self):
        # Quote "close" - reserved keyword in DuckDB
        simple_return_queries = ",\n                       ".join(
            [f'("close" / lag("close", {win}) over (partition by InnerCode order by TradingDay)) - 1 as simple_return_{win}' for win in self.windows]
        )
        simple_return_cols = ",\n                       ".join(
            [f'simple_return_{win}' for win in self.windows]
        )
        weighted_return_queries = ",\n                       ".join(
            [f'sum(turnover * pct_chg) over (partition by InnerCode order by TradingDay rows between {win - 1} preceding and current row) '
             f'/ nullif(sum(turnover) over (partition by InnerCode order by TradingDay rows between {win - 1} preceding and current row), 0) '
             f'as weighted_return_{win}' for win in self.windows]
        )


        duckdb.sql(
            f"""
            create or replace table momentum as
            with add_simple_return as (
                select InnerCode,
                       TradingDay,
                       "close",
                       {self.turnover_col} as turnover,
                       pct_chg / 100.0 as pct_chg,
                       {simple_return_queries}
                from stock_daily
            ),
            add_weighted_return as (
                select InnerCode,
                       TradingDay,
                       "close",
                       turnover,
                       pct_chg,
                       {simple_return_cols},
                       {weighted_return_queries}
                from add_simple_return
            )


            select * from add_weighted_return
            """
        )
        return 'momentum'

    def _run_func_onetime(self) -> str:
        self._load_data()
        return self._calculate_momentum_return()


    

