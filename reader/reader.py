'''
Author: Qimin Ma
Date: 2026-02-22 11:47:19
LastEditTime: 2026-02-24 19:45:11
FilePath: /Dataset/reader/reader.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
'''
Author: Qimin Ma
Date: 2026-02-22 11:47:19
LastEditTime: 2026-02-24 00:20:36
FilePath: /Dataset/reader/reader.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''

import duckdb
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
import tushare as ts

load_dotenv(find_dotenv())
DATAROOT = os.environ.get("DATAROOT")
TUSHARE_TOKEN = os.environ.get("TUSHARE_TOKEN")
pro = ts.pro_api(TUSHARE_TOKEN)

def _generate_date_range(start: str, end: str):
    # Normalize to YYYYMMDD string (callers may pass Timestamp; .replace on Timestamp raises "year must be integer")
    start_ymd = pd.Timestamp(start).strftime("%Y%m%d")
    end_ymd = pd.Timestamp(end).strftime("%Y%m%d")
    df_cal = pro.trade_cal(
        start_date=start_ymd,
        end_date=end_ymd,
        fields="cal_date",
        exchange="SSE",
        is_open=1,
    ).sort_values(by="cal_date")
    return df_cal["cal_date"].astype(str).str.replace("-", "").str[:8].values

def LoadConstant(db_name:str, 
                table_name:str,
                columns: list[str] = None, 
                condition: str = None,
                connection: duckdb.DuckDBPyConnection = None,
                duckdb_variable:str=None
                ):
    path = f"{DATAROOT}/{db_name}/constant/{table_name}.parquet"
    cols = ", ".join(columns) if columns else "*"
    where = f"{condition}" if condition else ""
    sql = f"SELECT {cols} FROM read_parquet('{path}'){where}"
    if duckdb_variable:
        if not connection:
            duckdb.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
            duckdb.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
        else:
            connection.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
            connection.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
    else:
        return duckdb.sql(sql) if not connection else connection.sql(sql)

def LoadDaily(
    db_name: str,
    table_name: str,
    start: str,
    end: str,
    columns: list[str] = None,
    condition: str = None,
    connection: duckdb.DuckDBPyConnection = None,
    duckdb_variable:str=None
    ):
    DIR = f"{DATAROOT}/{db_name}/{table_name}"
    date_list = _generate_date_range(start, end)
    paths = [f"'{DIR}/{d}.parquet'" for d in date_list]
    path = "[" + ", ".join(paths) + "]"
    if path == "[]":
        return duckdb.query("SELECT 1 AS _ LIMIT 0")
    cols = ", ".join(columns) if columns else "*"
    sql = f"SELECT {cols} FROM read_parquet({path}){condition}"
    if duckdb_variable:
        if not connection:
            duckdb.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
            duckdb.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
        else:
            connection.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
            connection.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
    else:
        return duckdb.sql(sql) if connection else duckdb.sql(sql)