'''
Author: Qimin Ma
Date: 2026-02-19 11:22:20
LastEditTime: 2026-02-24 20:48:58
FilePath: /Dataset/base.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from abc import ABC, abstractmethod
import logging
import os
from dotenv import load_dotenv, find_dotenv
from duckdb import table
import tushare as ts
from datetime import datetime
from tqdm import tqdm
import time
import pandas as pd
import re
import duckdb

# Calculate today data: YYYY-MM-DD
today = datetime.now().strftime('%Y-%m-%d')

DAILY_PARQUET_PATTERN = re.compile(r"^(\d{8})\.parquet$")
class TushareAPIError(Exception):
    """Raised when a Tushare API call fails after retries or returns invalid data."""

    pass


class DataValidationError(Exception):
    """Raised when required columns or data are missing or invalid."""

    pass


class Loader(ABC):
    def __init__(self, logger:logging.Logger, 
                db_name:str, 
                table_name:str, 
                max_retry:int=3,
                default_delays:list[int] = [1,2,4],
                ifsaved:bool = True
                ) -> None:

        """
        Args:
            logger: logging.Logger, the logger object
            db_name: str, the database name
            table_name: str, the table name
            max_retry: int, the maximum number of retries
            default_delays: list[int], the default delays

        The constant data loader is used to load the data without time dimension, such stock info, etc.
        """
        # Set the loader and check the environment variables
        self.logger = logger
        self._set_logger()
        self.max_retry = max_retry
        self.default_delays = default_delays
        if len(default_delays) != max_retry:
            self.logger.warning(f"The length of default_delays is not equal to max_retry, will use the first {max_retry} delays")
            self.default_delays = self.default_delays[:max_retry]
        self.ifsaved = ifsaved
        self.table_name = table_name

        # Connect to tushare API
        self._connect_tushare()

        # Make the data directory
        data_root = os.environ.get("DATAROOT")
        os.makedirs(data_root, exist_ok=True)
        self.data_dir = os.path.abspath(f"{data_root}/{db_name}")
        os.makedirs(self.data_dir, exist_ok=True)

    def _set_logger(self):
        try:
            load_dotenv(find_dotenv())
        except Exception as e:
            self.logger.error(f"Error loading environment variables: {e}")
            raise TushareAPIError(f"Error loading environment variables: {e}")

    def _connect_tushare(self):
        TUSHARE_TOKEN = os.environ.get("TUSHARE_TOKEN")
        self.logger.info(f"Tushare token loaded: {TUSHARE_TOKEN}")
        try:
            self.pro = ts.pro_api(TUSHARE_TOKEN)
        except Exception as e:
            self.logger.error(f"Error setting Tushare token: {e}")
            raise TushareAPIError(f"Error setting Tushare token: {e}")

# Load trading day
class TushareConstantLoader(Loader):
    def __init__(self, logger:logging.Logger, 
                db_name:str,
                table_name:str,
                max_retry:int=3,
                default_delays:list[int] = [1,2,4],
                ) -> None:
        super().__init__(logger, db_name, table_name, max_retry, default_delays)
        os.makedirs(f'{self.data_dir}/constant', exist_ok=True)
        self.run()

    def run(self):
        try:
            df = self._run_func_onetime()
            if df is not None and not df.empty:
                path = f"{self.data_dir}/constant/{self.table_name}.parquet"
                df.to_parquet(path, index=False)
                self.logger.info("Wrote %s -> %s (%d rows)", self.table_name, path, len(df))
        except Exception as e:
            self.logger.error("Error running %s: %s", self.table_name, e)
            raise TushareAPIError(f"Error running {self.table_name}: {e}")

    @abstractmethod
    def _run_func_onetime(self) -> pd.DataFrame:
        """Fetch data for one time and return as a single DataFrame."""
        pass


class TushareBigConstantLoader(Loader):
    def __init__(self, logger:logging.Logger, 
                db_name:str,
                table_name:str,
                max_retry:int=3,
                default_delays:list[int] = [1,2,4],
                ) -> None:
        super().__init__(logger, db_name, table_name, max_retry, default_delays)
        os.makedirs(f'{self.data_dir}/constant', exist_ok=True)
        self.run()

    def run(self):
        try:
            duckdb_name = self._run_func_onetime()
            path = f"{self.data_dir}/constant/{self.table_name}.parquet"
            if duckdb_name is not None:
                duckdb.sql(f"COPY {duckdb_name} TO '{path}' (FORMAT 'parquet')")
                self.logger.info("Created table %s from %s", duckdb_name, self.table_name)
        except Exception as e:
            self.logger.error("Error running %s: %s", self.table_name, e)
            raise TushareAPIError(f"Error running {self.table_name}: {e}")


    @abstractmethod
    def _run_func_onetime(self) -> str:
        """Fetch data for one time and return as a single DuckDB name."""
        pass

class TushareDailyLoader(Loader):
    def __init__(self, 
                logger: logging.Logger, 
                db_name:str,
                table_name:str,
                start:str='2015-01-01', 
                end:str=today,
                max_retry:int=3,
                default_delays:list[int] = [1,2,4],
                ifsaved:bool = True
                ) -> None:
        super().__init__(logger, db_name, table_name, max_retry, default_delays, ifsaved)

        self.start = start
        self.end = end
        os.makedirs(f"{self.data_dir}/{self.table_name}", exist_ok=True)

        self.logger.info("Loading data from %s to %s into %s", self.start, self.end, self.data_dir)
        self._date_range()
        self.missing_dates = self._check_missing_dates()
        
        if self.missing_dates:
            self.logger.info("Start running missing dates...")
            self.run()

    
    def _date_range(self):
        start_ymd = self.start.replace("-", "")[:8]
        end_ymd = self.end.replace("-", "")[:8]
        df_cal = self.pro.trade_cal(
            start_date=start_ymd,
            end_date=end_ymd,
            fields="cal_date",
            exchange="SSE",
            is_open=1,
        ).sort_values(by="cal_date")
        self.date_range = df_cal["cal_date"].astype(str).str.replace("-", "").str[:8].values


    def _get_existing_dates(self):
        dir_required = f"{self.data_dir}/{self.table_name}"
        if not os.path.isdir(dir_required):
            return set()
        existing = set()
        for name in os.listdir(dir_required):
            m = DAILY_PARQUET_PATTERN.match(name)
            if m:
                existing.add(m.group(1))
        return existing

    def _check_missing_dates(self):
        self.logger.info("Checking missing dates: date_range from calendar, existing from folder.")
        existing_dates = self._get_existing_dates()
        date_range_set = set(self.date_range)
        missing = sorted(date_range_set - existing_dates)
        if missing:
            self.logger.info(
                "There are %d missing dates in %s (existing %d in folder).",
                len(missing), self.table_name, len(existing_dates),
            )
            return missing
        self.logger.info("No missing data, no need to load.")
        return None

    def _run_single_date(self, date: str) -> pd.DataFrame:
        """Run loader for one date; returns DataFrame from _run_func_date_onetime."""
        self.logger.info(f"Running {self.table_name} for date: {date}")
        for i in range(self.max_retry):
            try:
                return self._run_func_date_onetime(date)
            except Exception as e:
                self.logger.error(f"Error running {self.table_name} for date: {date}, error: {e}")
                if i < self.max_retry - 1:
                    self.logger.info(f"Retry {i+1} of {self.max_retry} for {self.table_name} for date: {date}")
                    time.sleep(self.default_delays[i])
                else:
                    raise TushareAPIError(f"Error running {self.table_name} for date: {date}, error: {e}")

    def _daily_file_path(self, date: str) -> str:
        return f"{self.data_dir}/{self.table_name}/{date}.parquet"

    def run(self):
        for date in tqdm(self.missing_dates, desc=f"Running {self.table_name}"):
            try:
                df = self._run_single_date(date)
                if self.ifsaved:
                    if df is not None and not df.empty:
                        path = self._daily_file_path(date)
                        df.to_parquet(path, index=False)
                        self.logger.info("Wrote %s -> %s (%d rows)", date, path, len(df))
                    else:
                        return df
            except Exception as e:
                self.logger.error("Error running %s for date %s: %s", self.table_name, date, e)
                continue


    @abstractmethod
    def _run_func_date_onetime(self, date: str) -> pd.DataFrame:
        """Fetch data for one date and return as a single DataFrame."""
        pass



