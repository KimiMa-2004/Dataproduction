'''
Author: Qimin Ma
Date: 2026-02-21 16:39:01
LastEditTime: 2026-02-24 00:47:22
FilePath: /Dataset/stock_simple_factors/momentum.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from base import TushareDailyLoader, TushareConstantLoader
import logging
from datetime import datetime
import pandas as pd
import tushare as ts
import os
import duckdb
from reader import LoadDaily, LoadConstant


class Momentum(TushareDailyLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d'),
                windows:list[int]=[5, 21, 63, 126, 252]) -> None:
        self.windows = windows
        super().__init__(logger, 'momentum','momentum', "momentum", start=start, end=end, ifsaved=False)

    def cal_end(self, date:str):
        max_win = max(self.windows)
        tradingday = LoadConstant('raw_tushare','tradingday').df()

        # Calculate the date - max_win days before the date
        date = pd.to_datetime(date)
        # Find the index of the current date in the tradingday dataframe
        idx = tradingday[tradingday['TradingDay'] == date].index[0]
        # Calculate the index max_win days before
        target_idx = idx - max_win
        if target_idx < 0:
            raise ValueError(f"Not enough trading days before {date} to subtract {max_win} days.")
        return tradingday.iloc[target_idx]['TradingDay']

        return tradingday.iloc[-max_win].TradingDay

    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        end = self.cal_end(date)
        LoadDaily(db_name='raw_tushare', \
                table_name='stock_daily', \
                start=date, end=end, \
                columns=['InnerCode','TradingDay','close'], \
                duckdb_variable='stock_daily')
        LoadDaily(db_name='raw_tushare',
                table_name='index_daily',
                start=date, end=end, \
                columns=['TradingDay','close'], \
                condition="where InnerCode = '000852.SH'", # 中证1000 
                duckdb_variable='index_daily')

        duckdb.sql(f"""
            with (
            select a.*, b.close as index_close from stock_daily a
            left join index_daily b on and a.TradingDay = b.TradingDay   
            )
            as data_merged

            
        """)        

        
