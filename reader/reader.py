'''
Author: Qimin Ma
Date: 2026-02-22 11:47:19
LastEditTime: 2026-02-25 23:41:02
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


def _generate_date_range_fundamental(start:str, end:str):
    start_ymd = start.replace("-", "")[:8]
    end_ymd = end.replace("-", "")[:8]

    df_cal = pro.trade_cal(
        start_date=start_ymd,
        end_date=end_ymd,
        fields="cal_date",
        exchange="SSE",
        is_open=1,
    ).sort_values(by="cal_date")

    max_date = df_cal['cal_date'].max()
    start_year = start_ymd[:4]
    end_year = end_ymd[:4]

    required_lst = []
    for year in range(int(start_year), int(end_year)+1):
        for md in ['0331','0630','0930','1231']:
            date = f'{year}{md}'
            if date <= max_date:
                required_lst.append(date)
            else:
                break
    return required_lst

def LoadConstant(db_name:str, 
                table_name:str,
                columns: list[str] = None, 
                condition: str = None,
                connection: duckdb.DuckDBPyConnection = None,
                duckdb_variable:str=None,
                if_constant:bool=True
                ):
    if if_constant:
        path = f"{DATAROOT}/{db_name}/constant/{table_name}.parquet"
    else:
        path = f"{DATAROOT}/{db_name}/{table_name}/{table_name}.parquet"
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
    sql = f"SELECT {cols} FROM read_parquet({path}, union_by_name=true) {condition}"
    if duckdb_variable:
        if not connection:
            duckdb.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
            duckdb.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
        else:
            connection.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
            connection.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
    else:
        return duckdb.sql(sql) if connection else duckdb.sql(sql)


def LoadFundamental(
    db_name:str,
    table_name:str,
    start:str,
    end:str,
    columns:list[str]=None,
    condition:str=None,
    connection:duckdb.DuckDBPyConnection=None,
    duckdb_variable:str=None,
    if_ffill:bool=False
):
    DIR = f"{DATAROOT}/{db_name}/{table_name}"
    date_list = _generate_date_range_fundamental(start, end)
    paths = [f"'{DIR}/{d}.parquet'" for d in date_list]
    path = "[" + ", ".join(paths) + "]"
    if path == "[]":
        return duckdb.query("SELECT 1 AS _ LIMIT 0")
    cols = ", ".join(columns) if columns else "*"
    sql = f"SELECT {cols} FROM read_parquet({path}, union_by_name=true) {condition}"
    if not if_ffill:
        if duckdb_variable:
            if not connection:
                duckdb.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
                duckdb.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
            else:
                connection.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
                connection.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {sql}')
        else:
            return duckdb.sql(sql) if connection else duckdb.sql(sql)

    else:
        # 全量日频股票列表 (all_stocks) 与基本面 raw_data 同 connection，便于后续 as-of join
        LoadDaily(
            "raw_tushare",
            "stock_daily",
            start=start,
            end=end,
            columns=["TradingDay", "InnerCode"],
            connection=connection,
            duckdb_variable="all_stocks",
        )
        # As-of join：按 (InnerCode, TradingDay) 取「截至该交易日最近一次披露」的指标，
        # 等价于按 InnerCode 分组做前向填充；从未披露的公司指标保持 NULL，下游可按需过滤。
        query = f"""
        WITH raw_data AS ({sql}),
        latest_report AS (
            SELECT
                a.InnerCode,
                a.TradingDay,
                (SELECT MAX(b.f_ann_date)
                 FROM raw_data b
                 WHERE b.InnerCode = a.InnerCode
                   AND b.f_ann_date <= a.TradingDay) AS latest_f_ann_date
            FROM all_stocks a
        )
        SELECT
            lr.InnerCode,
            lr.TradingDay,
            r.* EXCLUDE (InnerCode, f_ann_date)
        FROM latest_report lr
        LEFT JOIN raw_data r
            ON r.InnerCode = lr.InnerCode
           AND r.f_ann_date = lr.latest_f_ann_date
        ORDER BY lr.InnerCode, lr.TradingDay
        """

        if duckdb_variable:
            if not connection:
                duckdb.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
                duckdb.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {query}')
            else:
                connection.sql(f'DROP TABLE IF EXISTS {duckdb_variable}')
                connection.sql(f'CREATE TABLE IF NOT EXISTS {duckdb_variable} AS {query}')
        else:
            return duckdb.sql(query) if connection else duckdb.sql(query)