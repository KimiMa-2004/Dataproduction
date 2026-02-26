from base import TushareBigConstantLoader
import logging
from datetime import datetime
from typing import Literal
import duckdb
from reader import LoadDaily


class Volatility(TushareBigConstantLoader):
    def __init__(self, logger: logging.Logger, 
                start:str='2015-01-01', 
                end:str=datetime.now().strftime('%Y-%m-%d'),
                windows:list[int]=[5, 21, 63, 126, 252]) -> None:
        self.start = start
        self.end = end
        self.windows = windows
        super().__init__(logger, db_name='stock_classic_factors', table_name='volatility')

    def _run_func_onetime(self) -> str:
        LoadDaily(
            db_name='raw_tushare',
            table_name='stock_daily',
            start=self.start,
            end=self.end,
            columns=['InnerCode', 'TradingDay', 'close', 'pct_chg'],
            duckdb_variable='stock_daily'
        )
        volatility_cols = ", ".join(f"stddev(pct_chg) over (partition by InnerCode \
            order by TradingDay rows between {w - 1} preceding and current row) as volatility_{w}" \
                for w in self.windows)
        duckdb.sql(f"""
            create or replace table volatility as
            select InnerCode, TradingDay, {volatility_cols}
            from stock_daily
        """)
        return 'volatility'