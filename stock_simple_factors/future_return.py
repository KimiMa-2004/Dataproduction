'''
Author: Qimin Ma
Date: 2026-02-26 12:33:16
LastEditTime: 2026-02-26 18:09:00
FilePath: /Dataset/stock_simple_factors/future_return.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from base import TushareBigConstantLoader
import logging
from datetime import datetime
from typing import Literal
import duckdb
from reader import LoadDaily


class FutureReturn(TushareBigConstantLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d'),
                windows:list[int]=[5, 21, 63, 126, 252]) -> None:

        # Each window means the return between T+1 close and T+1+window close
        self.start = start
        self.end = end
        self.windows = windows
        super().__init__(logger, db_name='stock_classic_factors', table_name='future_return')

    def _run_func_onetime(self) -> str:
        LoadDaily(
            db_name='raw_tushare',
            table_name='stock_daily',
            start=self.start,
            end=self.end,
            columns=['InnerCode', 'TradingDay', 'close'],
            duckdb_variable='stock_daily'
        )
        # T 日记录的 future_return_win = (T+1+win 收盘价 / T+1 收盘价) - 1，用于深度学习预测标签
        future_return_cols = ", ".join(
            [f"""(lead("close", {1 + w}) over (partition by InnerCode order by TradingDay) 
            / lead("close", 1) over (partition by InnerCode order by TradingDay)) - 1 as future_return_{w}"""
             for w in self.windows]
        )
        duckdb.sql(f"""
            create or replace table future_return as
            select InnerCode, TradingDay, {future_return_cols}, close
            from stock_daily
        """)
        return 'future_return'