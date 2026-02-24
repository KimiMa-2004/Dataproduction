from base import TushareDailyLoader, TushareConstantLoader
import logging
from datetime import datetime
import pandas as pd
import tushare as ts
from reader import LoadDaily



class Evaluate(TushareDailyLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d')) -> None:
        super().__init__(logger, db_name='raw_tushare', table_name='stock_daily', start=start, end=end)

    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        LoadDaily(
            db_name='raw_tushare',
            table_name="stock_daily",
            start=date,
            end=date,
            columns=['InnerCode','TradingDay','pe','pe_ttm','pb','ps_ttm',]

        )