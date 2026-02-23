'''
Author: Qimin Ma
Date: 2026-02-21 16:39:01
LastEditTime: 2026-02-24 00:04:10
FilePath: /Dataset/raw_tushare/stock_daily.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from base import TushareDailyLoader, TushareConstantLoader
import logging
from datetime import datetime
import pandas as pd
import tushare as ts



class StockDaily(TushareDailyLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='stock_daily', start=start, end=end)

    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        return_daily = self.pro.daily(trade_date=date)
        daily_basic = self.pro.daily_basic(trade_date=date).drop(columns=['close'])
        data = pd.merge(return_daily, daily_basic, on=['ts_code','trade_date'], how='left')
        stock_info = self.pro.stock_basic()
        data = pd.merge(data, stock_info, on=['ts_code'], how='left').rename(columns={'ts_code':'InnerCode','trade_date':'TradingDay'})
        data['TradingDay'] = pd.to_datetime(data['TradingDay'])
        return data


class StockInfo(TushareConstantLoader):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='stock_info')

    def _run_func_onetime(self) -> pd.DataFrame:
        df = self.pro.stock_basic().rename(columns={'ts_code':'InnerCode'})
        return df


