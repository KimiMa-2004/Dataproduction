'''
Author: Qimin Ma
Date: 2026-02-19 12:24:10
LastEditTime: 2026-02-23 22:58:40
FilePath: /Dataset/main.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
from raw_tushare.stock_daily import StockDaily, StockInfo
from raw_tushare.index import IndexDaily, IndexInfo
from smart_data_loader.logger import get_logger

if __name__ == "__main__":
    # Load stock data
    logger = get_logger(name='stock_loader', filename='stock',ifconsole=False)
    _ = StockInfo(logger)
    _ = StockDaily(logger, start='2015-01-01')

    logger = get_logger(name='index_loader', filename='index',ifconsole=False)
    _ = IndexInfo(logger)
    _ = IndexDaily(logger, start='2015-01-01')
    