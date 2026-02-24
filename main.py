'''
Author: Qimin Ma
Date: 2026-02-19 12:24:10
LastEditTime: 2026-02-24 21:51:55
FilePath: /Dataset/main.py
Description: 
Copyright (c) 2026 by Qimin Ma, All Rights Reserved.
'''
import raw_tushare
from smart_data_loader.logger import get_logger
import stock_simple_factors

if __name__ == "__main__":
    # Load stock data
    logger = get_logger(name='stock_loader', filename='stock',ifconsole=False)
    _ = raw_tushare.StockInfo(logger)
    _ = raw_tushare.StockDaily(logger, start='2015-01-01')

    logger = get_logger(name='index_loader', filename='index',ifconsole=False)
    _ = raw_tushare.IndexInfo(logger)
    _ = raw_tushare.IndexDaily(logger)
    _ = raw_tushare.IndexReturn(logger)

    logger = get_logger(name='tradingday_loader', filename='tradingday',ifconsole=False)
    _ = raw_tushare.TradingDay(logger)
    
    logger = get_logger(name='momentum_loader', filename='simple_stock_factors', ifconsole=False)
    _ = stock_simple_factors.Momentum(logger, start='2015-01-01', turnover_type="turnover_rate")
