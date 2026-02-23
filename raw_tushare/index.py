'''
Author: Qimin Ma
Date: 2026-02-21 16:39:01
LastEditTime: 2026-02-23 22:55:40
FilePath: /Dataset/raw_tushare/index.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from .base import TushareDailyLoader, TushareConstantLoader
import logging
from datetime import datetime
import pandas as pd
import tushare as ts
import os



class IndexDaily(TushareDailyLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        self.code_list = ['000001.SH', '000300.SH', '000852.SH']
        super().__init__(logger, 'index','index_daily', "IndexDaily", start=start, end=end)
        

    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        data = self.pro.index_dailybasic(trade_date=date)
        index_info = self.pro.index_basic()
        data = pd.merge(data, index_info, on=['ts_code'], how='left').\
            rename(columns={'ts_code':'InnerCode','trade_date':'TradingDay'})
        data['TradingDay'] = pd.to_datetime(data['TradingDay'])
        return data


class IndexInfo(TushareConstantLoader):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(logger, 'index','index_info', "IndexInfo")

    def _run_func_onetime(self) -> pd.DataFrame:
        df = self.pro.index_basic().rename(columns={'ts_code':'InnerCode'})
        return df