'''
华泰单因子测试—成长因子 (Growth Factors)，合并为一张表。
列名与计算口径严格按 description.md 中 raw_tushare 表结构。
'''
from base import TushareBigConstantLoader
import logging
from datetime import datetime
import pandas as pd
import duckdb
from reader import LoadDaily, LoadFundamental
from smart_data_loader.fundamental.fundamental import FundamentalPreprocessor

# 成长因子定义（华泰单因子测试—成长因子及其描述）
# 具体因子              因子描述
# Sales_G_q            当季营业收入 (最新财报) 同比增长率
# Sales_G_ttm         营业收入 (TTM) 同比增长率
# Sales_G_3y          营业收入 (TTM) 三年复合增长率
# Profit_G_q          当季净利润 (最新财报) 同比增长率
# Profit_G_ttm        净利润 (TTM) 同比增长率
# Profit_G_3y          净利润 (TTM) 三年复合增长率
# OCF_G_q             当季经营性现金流 (最新财报) 同比增长率
# OCF_G_ttm           经营性现金流 (TTM) 同比增长率
# OCF_G_3y            经营性现金流 (TTM) 三年复合增长率
# ROE_G_q             当季 ROE (最新财报) 同比增长率
# ROE_G_ttm           ROE (TTM) 同比增长率
# ROE_G_3y            ROE (TTM) 三年复合增长率

YOY_DAILY_PERIOD = 252   # 日频下“去年同期”约 252 个交易日
THREE_YEAR_DAYS = 756    # 252 * 3，用于三年复合


class Growth(TushareBigConstantLoader):
    def __init__(
        self,
        logger: logging.Logger,
        start: str = '2015-01-01',
        end: str = None,
    ) -> None:
        self.start = start
        self.end = end or datetime.now().strftime('%Y-%m-%d')
        super().__init__(logger, db_name='stock_classic_factors', table_name='growth')

    def _run_func_onetime(self) -> str:

        # 1) 全量日频
        LoadDaily(
            db_name='raw_tushare',
            table_name='stock_daily',
            start=self.start,
            end=self.end,
            columns=['InnerCode', 'TradingDay'],
            duckdb_variable='all_stocks',
        )

        # 2) 基本面原始表（description.md 列名）
        # income: 营业收入 revenue, 净利润 n_income
        LoadFundamental(
            db_name='raw_tushare',
            table_name='income',
            start=self.start,
            end=self.end,
            columns=['InnerCode', 'f_ann_date', 'revenue', 'n_income'],
            duckdb_variable='income_raw',
        )
        # cashflow: 经营活动产生的现金流量净额 n_cashflow_act
        LoadFundamental(
            db_name='raw_tushare',
            table_name='cashflow',
            start=self.start,
            end=self.end,
            columns=['InnerCode', 'f_ann_date', 'n_cashflow_act'],
            duckdb_variable='cashflow_raw',
        )
        # fina_indicator: 报告期 end_date；roe 及 yoy（%）。列名以 description.md 为准，仅有 q_sales_yoy 为单季度同比
        LoadFundamental(
            db_name='raw_tushare',
            table_name='fina_indicator',
            start=self.start,
            end=self.end,
            columns=[
                'InnerCode', 'end_date',
                'roe', 'tr_yoy', 'netprofit_yoy', 'ocf_yoy', 'roe_yoy',
                'q_sales_yoy',
            ],
            duckdb_variable='fina_raw',
        )

        # 3) 合并到日频 + 前向填充 + TTM（日频 252 日均）
        # income
        income_pp = FundamentalPreprocessor(
            logger=self.logger,
            fundamental_table='income_raw',
            all_stock_table='all_stocks',
            merging_date_type='f_ann_date',
        )
        income_pp.ffill_na()
        income_pp.cal_ttm_mean(['revenue', 'n_income'], window=YOY_DAILY_PERIOD)
        duckdb.register('income_daily', income_pp.merge_df)
        duckdb.sql("CREATE OR REPLACE TABLE income_daily AS SELECT * FROM income_daily")

        # cashflow
        cashflow_pp = FundamentalPreprocessor(
            logger=self.logger,
            fundamental_table='cashflow_raw',
            all_stock_table='all_stocks',
            merging_date_type='f_ann_date',
        )
        cashflow_pp.ffill_na()
        cashflow_pp.cal_ttm_mean(['n_cashflow_act'], window=YOY_DAILY_PERIOD)
        duckdb.register('cashflow_daily', cashflow_pp.merge_df)
        duckdb.sql("CREATE OR REPLACE TABLE cashflow_daily AS SELECT * FROM cashflow_daily")

        # fina_indicator（按报告期 end_date 合并）
        fina_pp = FundamentalPreprocessor(
            logger=self.logger,
            fundamental_table='fina_raw',
            all_stock_table='all_stocks',
            merging_date_type='end_date',
        )
        fina_pp.ffill_na()
        fina_pp.cal_ttm_mean(['roe'], window=YOY_DAILY_PERIOD)
        duckdb.register('fina_daily', fina_pp.merge_df)
        duckdb.sql("CREATE OR REPLACE TABLE fina_daily AS SELECT * FROM fina_daily")

        # 4) 合并为成长因子表（华泰 12 个因子）
        # 列名按 description.md：仅 q_sales_yoy 为单季度同比，其余 _q 用 TTM 同比顶替
        duckdb.sql(f"""
        CREATE OR REPLACE TABLE growth AS
        WITH base AS (
            SELECT a.InnerCode, a.TradingDay,
                   i.revenue, i.n_income, i.revenue_ttm, i.n_income_ttm,
                   c.n_cashflow_act, c.n_cashflow_act_ttm,
                   f.roe, f.roe_ttm,
                   f.tr_yoy, f.netprofit_yoy, f.ocf_yoy, f.roe_yoy,
                   f.q_sales_yoy
            FROM all_stocks a
            LEFT JOIN income_daily i ON a.InnerCode = i.InnerCode AND a.TradingDay = i.TradingDay
            LEFT JOIN cashflow_daily c ON a.InnerCode = c.InnerCode AND a.TradingDay = c.TradingDay
            LEFT JOIN fina_daily f ON a.InnerCode = f.InnerCode AND a.TradingDay = f.TradingDay
        ),
        with_lag AS (
            SELECT *,
                   lag(revenue_ttm, {THREE_YEAR_DAYS}) OVER w AS revenue_ttm_3y,
                   lag(n_income_ttm, {THREE_YEAR_DAYS}) OVER w AS n_income_ttm_3y,
                   lag(n_cashflow_act_ttm, {THREE_YEAR_DAYS}) OVER w AS n_cashflow_act_ttm_3y,
                   lag(roe_ttm, {THREE_YEAR_DAYS}) OVER w AS roe_ttm_3y
            FROM base
            WINDOW w AS (PARTITION BY InnerCode ORDER BY TradingDay)
        )
        SELECT
            InnerCode,
            TradingDay,
            q_sales_yoy    AS Sales_G_q,
            tr_yoy         AS Sales_G_ttm,
            (revenue_ttm / nullif(revenue_ttm_3y, 0))^(1.0/3.0) - 1 AS Sales_G_3y,
            netprofit_yoy  AS Profit_G_q,
            netprofit_yoy  AS Profit_G_ttm,
            (n_income_ttm / nullif(n_income_ttm_3y, 0))^(1.0/3.0) - 1 AS Profit_G_3y,
            ocf_yoy        AS OCF_G_q,
            ocf_yoy        AS OCF_G_ttm,
            (n_cashflow_act_ttm / nullif(n_cashflow_act_ttm_3y, 0))^(1.0/3.0) - 1 AS OCF_G_3y,
            roe_yoy        AS ROE_G_q,
            roe_yoy        AS ROE_G_ttm,
            (roe_ttm / nullif(roe_ttm_3y, 0))^(1.0/3.0) - 1 AS ROE_G_3y
        FROM with_lag
        ORDER BY InnerCode, TradingDay
        """)

        return "growth"
