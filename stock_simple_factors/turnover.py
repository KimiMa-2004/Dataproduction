"""
华泰单因子测试——换手率因子。
基于 stock_daily 的日换手率（turnover_rate 或 f_turnover_rate）计算：
turn_Nm、bias_turn_Nm、std_turn_Nm、bias_std_turn_Nm（N=1,3,6）。
"""
from base import TushareBigConstantLoader
import logging
from datetime import datetime
from typing import Literal
import duckdb
from reader import LoadDaily


# 1m/3m/6m 对应约 21/63/126 个交易日，2 年约 504
TURNOVER_SHORT_WINDOWS = [21, 63, 126]
TURNOVER_LONG_WINDOW = 504
TURNOVER_SUFFIXES = {21: "1m", 63: "3m", 126: "6m"}


def _turn_suffix(w: int) -> str:
    """窗口 w 对应的列后缀，如 21 -> '1m'，5 -> '5m'。"""
    return TURNOVER_SUFFIXES.get(w, f"{w}m")


class Turnover(TushareBigConstantLoader):
    """换手率因子：日均换手率、相对 2 年均值的偏离、波动及相对波动。"""

    def __init__(
        self,
        logger: logging.Logger,
        start: str = '2015-01-01',
        end: str = None,
        windows: list[int] = None,
        long_window: int = TURNOVER_LONG_WINDOW,
        turnover_col: Literal['turnover_rate', 'f_turnover_rate'] = 'turnover_rate',
    ) -> None:
        """
        Args:
            logger: 日志。
            start: 开始日期。
            end: 结束日期，默认当前日。
            windows: 短期窗口（交易日），默认 [21, 63, 126] 对应 1m/3m/6m。
            long_window: 长期窗口（2 年约 504 日），用于 bias 类因子。
            turnover_col: 使用的日换手率列，'turnover_rate' 或 'f_turnover_rate'（来自 stock_daily）。
        """
        self.start = start
        self.end = end or datetime.now().strftime('%Y-%m-%d')
        self.windows = windows if windows is not None else TURNOVER_SHORT_WINDOWS.copy()
        self.long_window = long_window
        self.turnover_col = turnover_col
        super().__init__(logger, db_name='stock_classic_factors', table_name='turnover')

    def _run_func_onetime(self) -> str:
        LoadDaily(
            db_name='raw_tushare',
            table_name='stock_daily',
            start=self.start,
            end=self.end,
            columns=['InnerCode', 'TradingDay', self.turnover_col],
            duckdb_variable='stock_daily',
        )
        # 用 DuckDB 窗口函数计算：短期 mean/std、长期 mean/std，再算 bias
        mean_short = ", ".join(
            f"avg({self.turnover_col}) over (partition by InnerCode order by TradingDay rows between {w - 1} preceding and current row) as turn_{_turn_suffix(w)}"
            for w in self.windows
        )
        std_short = ", ".join(
            f"stddev({self.turnover_col}) over (partition by InnerCode order by TradingDay rows between {w - 1} preceding and current row) as std_turn_{_turn_suffix(w)}"
            for w in self.windows
        )
        select_step1 = f"""
            InnerCode, TradingDay,
            avg({self.turnover_col}) over (partition by InnerCode order by TradingDay rows between {self.long_window - 1} preceding and current row) as turn_2y,
            stddev({self.turnover_col}) over (partition by InnerCode order by TradingDay rows between {self.long_window - 1} preceding and current row) as std_turn_2y,
            {mean_short},
            {std_short}
        """
        bias_turn = ", ".join(
            f"(t.turn_{_turn_suffix(w)} / nullif(t.turn_2y, 0)) - 1 as bias_turn_{_turn_suffix(w)}"
            for w in self.windows
        )
        bias_std_turn = ", ".join(
            f"(t.std_turn_{_turn_suffix(w)} / nullif(t.std_turn_2y, 0)) - 1 as bias_std_turn_{_turn_suffix(w)}"
            for w in self.windows
        )
        turn_cols = ", ".join(f"t.turn_{_turn_suffix(w)}" for w in self.windows)
        std_cols = ", ".join(f"t.std_turn_{_turn_suffix(w)}" for w in self.windows)

        duckdb.sql(f"""
            create or replace table turnover as
            with step1 as (
                select {select_step1}
                from stock_daily
            ),
            t as (
                select * from step1
            )
            select t.InnerCode,
                   t.TradingDay,
                   {turn_cols},
                   {bias_turn},
                   {std_cols},
                   {bias_std_turn}
            from t
        """)
        self.logger.info("Turnover factors computed with turnover_col=%s", self.turnover_col)
        return 'turnover'
