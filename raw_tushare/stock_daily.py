'''
Author: Qimin Ma
Date: 2026-02-21 16:39:01
LastEditTime: 2026-02-26 11:45:36
FilePath: /Dataset/raw_tushare/stock_daily.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''

from abc import abstractmethod
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


class FundamentalLoader(TushareDailyLoader):
    def __init__(self, logger: logging.Logger, 
                db_name:str,
                table_name:str,
                start_year:int=2015, 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        self.start_year = start_year
        super().__init__(logger, db_name=db_name, table_name=table_name, start=f"{start_year}-01-01", end=end)
    
    @abstractmethod
    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        pass

    def _date_range(self):
        start_ymd = f'{self.start_year}0101'
        end_ymd = self.end.replace("-", "")[:8]
        df_cal = self.pro.trade_cal(
            start_date=start_ymd,
            end_date=end_ymd,
            fields="cal_date",
            exchange="SSE",
            is_open=1,
        ).sort_values(by="cal_date")

        max_date = df_cal['cal_date'].max()
        end_year = end_ymd[:4]

        required_lst = []
        for year in range(self.start_year, int(end_year)):
            for md in ['0331','0630','0930','1231']:
                date = f'{year}{md}'
                if date <= max_date:
                    required_lst.append(date)
                else:
                    break
        self.date_range = required_lst


class Income(FundamentalLoader):
    def __init__(self, logger: logging.Logger, 
                start:int=2015, 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='income', start_year=start, end=end)
    
    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        df = self.pro.income_vip(period=date)
        df.rename(columns={'ts_code':'InnerCode'}, inplace=True)
        df['f_ann_date'] = pd.to_datetime(df['f_ann_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['ann_date'] = pd.to_datetime(df['ann_date'])
        return df


class Balance(FundamentalLoader):
    def __init__(self, logger: logging.Logger, 
                start:int=2015, 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='balance', start_year=start, end=end)
    
    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        df = self.pro.balancesheet_vip(period=date)
        df.rename(columns={'ts_code':'InnerCode'}, inplace=True)
        df['f_ann_date'] = pd.to_datetime(df['f_ann_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['ann_date'] = pd.to_datetime(df['ann_date'])
        return df


class CashFlow(FundamentalLoader):
    def __init__(self, logger: logging.Logger, 
                start:int=2015, 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='cashflow', start_year=start, end=end)
    
    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        df = self.pro.cashflow_vip(period=date)
        df.rename(columns={'ts_code':'InnerCode'}, inplace=True)
        df['f_ann_date'] = pd.to_datetime(df['f_ann_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['ann_date'] = pd.to_datetime(df['ann_date'])
        return df


class FinaIndicator(FundamentalLoader):
    def __init__(self, logger: logging.Logger, 
                start:int=2015, 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='fina_indicator', start_year=start, end=end)
    
    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        df = self.pro.fina_indicator_vip(period=date)
        df.rename(columns={'ts_code':'InnerCode'}, inplace=True)
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['ann_date'] = pd.to_datetime(df['ann_date'])
        return df