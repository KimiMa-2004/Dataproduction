'''
Author: Qimin Ma
Date: 2026-02-19 12:24:10
LastEditTime: 2026-02-24 00:27:40
FilePath: /Dataset/main.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
import raw_tushare
from smart_data_loader.logger import get_logger

if __name__ == "__main__":
    # Load stock data
    logger = get_logger(name='stock_loader', filename='stock',ifconsole=False)
    _ = raw_tushare.StockInfo(logger)
    _ = raw_tushare.StockDaily(logger, start='2015-01-01')

    logger = get_logger(name='index_loader', filename='index',ifconsole=False)
    _ = raw_tushare.IndexInfo(logger)
    _ = raw_tushare.IndexDaily(logger, start='2014-12-31')

    logger = get_logger(name='tradingday_loader', filename='tradingday',ifconsole=False)
    _ = raw_tushare.TradingDay(logger)
    