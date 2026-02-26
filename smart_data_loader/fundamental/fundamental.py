import duckdb
import pandas as pd
import logging


class FundamentalPreprocessor(object):
    def __init__(self, \
                logger:logging.Logger, \
                fundamental_table:str, \
                all_stock_table:str, \
                merging_date_type:str='f_ann_date',
                ):

        self.logger = logger
        self.merge_df = duckdb.sql(f""" 
                select a.InnerCode, a.TradingDay, b.* EXCLUDE (InnerCode, {merging_date_type})
                from {all_stock_table} a
                left join {fundamental_table} b
                on a.InnerCode = b.InnerCode and a.TradingDay = b.{merging_date_type}
                order by a.InnerCode, a.TradingDay
                """).df()
        self.logger.info(f"Finish merging {fundamental_table} and {all_stock_table}")


    def ffill_na(self):
        """按 InnerCode 分组对合并表做前向填充；某资产在某列全为空时保持 NaN。"""
        df = self.merge_df.copy()
        key_cols = ["InnerCode", "TradingDay"]
        fill_cols = [c for c in df.columns if c not in key_cols]
        if not fill_cols:
            self.logger.warning("No columns to forward-fill.")
            return

        # 按 InnerCode 分组前向填充；整列全空时 ffill 不产生新值，保持 NaN
        df[fill_cols] = df.groupby("InnerCode", group_keys=False)[fill_cols].ffill()
        self.logger.info("Finished forward-fill by InnerCode.")
        self.merge_df = df
        return df

    def interpolate_na(self, method:str="linear"):
        """按 InnerCode 分组对合并表做线性插值；某资产在某列全为空时保持 NaN。"""
        df = self.merge_df.copy()
        key_cols = ["InnerCode", "TradingDay"]
        fill_cols = [c for c in df.columns if c not in key_cols]
        if not fill_cols:
            self.logger.warning("No columns to interpolate.")
            return
        df[fill_cols] = df.groupby("InnerCode", group_keys=False)[fill_cols].interpolate(method=method)
        self.logger.info("Finished interpolate by InnerCode.")
        self.merge_df = df

    
    def backward_fill_na(self):
        """按 InnerCode 分组对合并表做后向填充；某资产在某列全为空时保持 NaN。"""
        df = self.merge_df.copy()
        key_cols = ["InnerCode", "TradingDay","f_ann_date","ann_date","end_date"]
        fill_cols = [c for c in df.columns if c not in key_cols]
        if not fill_cols:
            self.logger.warning("No columns to backward-fill.")
            return
        df[fill_cols] = df.groupby("InnerCode", group_keys=False)[fill_cols].bfill()
        self.logger.info("Finished backward-fill by InnerCode.")
        self.merge_df = df

    def cal_ttm(self, ttm_cols:list[str], windows:int=252):
        """计算 TTM 指标。ttm为过去252天均值, 如果不足则直接返回NAN"""
        df = self.merge_df.copy()
        for col in ttm_cols:
            df[f'{col}_ttm'] = df.groupby("InnerCode", group_keys=False)[col].\
                transform(lambda x: x.rolling(window=windows).mean() if len(x) >= windows else None)
        self.logger.info("Finished calculate TTM.")
        self.merge_df = df  
    
    def cal_ttm_mean(self, ttm_cols:list[str], window:int=252):
        """计算 TTM 指标。ttm为过去window天均值, 如果不足则直接返回NAN"""
        df = self.merge_df.copy()
        for col in ttm_cols:
            df[f'{col}_ttm'] = df.groupby("InnerCode", group_keys=False)[col].\
                transform(lambda x: x.rolling(window=window).mean() if len(x) >= window else None)
        self.logger.info(f"Finished calculate TTM with window {window}.")
        self.merge_df = df

    def growth_rate(self, columns: list[str], period: int = 252):
        """计算指定列的同比/环比增长率（当期 vs 去年同期）。
        公式: (当期 - 去年同期) / 去年同期；去年同期由 period 期前表示。
        同比：季频基本面常用 period=4；日频可用 period=252。
        环比：季频基本面常用 period=1；日频可用 period=63。
        某资产某列无去年同期值时结果为 NaN。"""
        df = self.merge_df.copy()
        key_cols = ["InnerCode", "TradingDay"]
        fill_cols = [c for c in columns if c in df.columns and c not in key_cols]
        if not fill_cols:
            self.logger.warning("No valid columns for YoY growth rate.")
            return df
        for col in fill_cols:
            lag_col = df.groupby("InnerCode", group_keys=False)[col].shift(period)
            df[f"{col}_yoy"] = (df[col] - lag_col) / lag_col
        self.logger.info(f"Finished YoY growth rate for {fill_cols} (period={period}).")
        self.merge_df = df


