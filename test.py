from stock_simple_factors.future_return import FutureReturn
from smart_data_loader.logger import get_logger

if __name__ == "__main__":
    future_return = FutureReturn(logger=get_logger(name='future_return', filename='future_return',ifconsole=True),
                                start='2015-01-01', end='2026-02-25', windows=[2, 3])
    