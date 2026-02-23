'''
Author: Qimin Ma
Date: 2026-02-21 16:39:01
LastEditTime: 2026-02-24 00:33:38
FilePath: /Dataset/raw_tushare/tradingday.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from base import TushareDailyLoader, TushareConstantLoader
import logging
from datetime import datetime
import pandas as pd
import tushare as ts

today = datetime.now().strftime('%Y-%m-%d')

class TradingDay(TushareConstantLoader):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='tradingday')

    def _run_func_onetime(self) -> pd.DataFrame:
        df = self.pro.trade_cal(exchange='SSE', is_open='1', start_date='20150101', end_date=today.replace("-", "")[:8],
                            fields='cal_date').rename(columns={'cal_date':'TradingDay'}).sort_values(by='TradingDay').reset_index(drop=True)
        df['TradingDay'] = pd.to_datetime(df['TradingDay'])
        return df