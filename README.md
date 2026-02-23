# Daily Data Import Template

A small template for **daily (and constant) financial data import** from [Tushare](https://tushare.pro). Data is stored as **one Parquet file per trading day** under a configurable root, and can be read back with **DuckDB** for analysis.

---

## Purpose

- **Ingest** daily time-series and one-off “constant” datasets (e.g. stock list, index list) from the Tushare API.
- **Store** daily data as `YYYYMMDD.parquet` in a folder so that:
  - Only missing dates are fetched on each run.
  - You can later read only a date range without scanning the whole history.
- **Read** data via DuckDB (e.g. `LoadDaily`, `LoadConstant`) for downstream use.

---

## Architecture

```
Dataset/
├── main.py                 # Entry: run stock & index loaders
├── raw_tushare/             # Tushare data ingestion
│   ├── base.py              # Base classes: Loader, TushareConstantLoader, TushareDailyLoader
│   ├── stock_daily.py       # StockDaily, StockInfo
│   └── index.py             # IndexDaily, IndexInfo
├── reader/
│   └── reader.py            # LoadConstant, LoadDaily (DuckDB)
├── smart_data_loader/
│   └── logger/              # Logging (get_logger, etc.)
└── (logs, .env, etc.)
```

- **`raw_tushare.base`**  
  - **Loader**: base with env, Tushare connection, and data directory setup.  
  - **TushareConstantLoader**: one-off fetch → single Parquet (e.g. `StockInfo.parquet`).  
  - **TushareDailyLoader**: uses Tushare trading calendar for a `start`–`end` range, scans the target folder for existing `YYYYMMDD.parquet` files, computes **missing_dates**, then fetches and writes **one Parquet per missing day**.

- **`raw_tushare.stock_daily` / `index`**  
  Concrete loaders: they call the Tushare API and return a DataFrame for one date (daily) or once (constant). You can add more loaders by subclassing `TushareDailyLoader` or `TushareConstantLoader` and implementing the abstract fetch method.

- **`reader.reader`**  
  - **LoadConstant**: read a single Parquet (e.g. stock/info table).  
  - **LoadDaily**: for a `start`–`end` range, build the list of `YYYYMMDD.parquet` paths in that range and use DuckDB’s `read_parquet(list_of_paths)` so only those days are scanned.

- **Data layout**  
  Under `DATAROOT` (from `.env`):
  - Daily: `{DATAROOT}/{category}/{dir_name}/YYYYMMDD.parquet` (e.g. `.../stock/stock_daily/20260101.parquet`).
  - Constant: `{DATAROOT}/{category}/{dir_name}/{data_name}.parquet` (e.g. `.../stock/stock_info/StockInfo.parquet`).

---

## Requirements

- Python 3.x
- Tushare account and API token
- Dependencies: `pandas`, `duckdb`, `tushare`, `python-dotenv`, `tqdm` (and any used by the logger)

---

## Setup

1. **Environment variables** (e.g. in a `.env` file at the project root, not committed):

   - `TUSHARE_TOKEN`: your Tushare API token.  
   - `DATAROOT`: root directory for all output Parquet files (e.g. `D:/Aether/FinancialData` or `./Data`).

2. Install dependencies (e.g. `pip install pandas duckdb tushare python-dotenv tqdm`).

---

## How to Use

### Running the import (main entry)

From the project root:

```bash
python main.py
```

This uses the configured logger and runs, for example:

- **Stock**: `StockInfo` (constant), then `StockDaily` (daily in a date range).
- **Index**: `IndexInfo` (constant), then `IndexDaily` (daily in a date range).

Each daily loader:

1. Gets the trading-day range from Tushare for `start`–`end`.
2. Scans its folder for existing `YYYYMMDD.parquet` files.
3. Fetches only **missing** dates and writes one Parquet per day.

### Using the loaders in code

```python
from smart_data_loader.logger import get_logger
from raw_tushare.stock_daily import StockDaily, StockInfo
from raw_tushare.index import IndexDaily, IndexInfo

logger = get_logger(name='stock_loader', filename='stock', ifconsole=False)

# One-off: stock list
_ = StockInfo(logger)

# Daily: fill missing days from 2015-01-01 to today (default)
_ = StockDaily(logger, start='2015-01-01')

# Or with an explicit end date
_ = StockDaily(logger, start='2025-01-01', end='2026-01-10')
```

Same idea for `IndexInfo` and `IndexDaily` with their own logger/names.

### Reading data back (DuckDB)

```python
from reader.reader import LoadDaily, LoadConstant

# Daily: only files in [start, end] are scanned (trading days)
rel = LoadDaily('stock', 'stock_daily', start='2026-01-01', end='2026-01-10')
df = rel.df()  # or use the DuckDB relation in SQL

# Optional: columns and condition
rel = LoadDaily('stock', 'stock_daily', start='2026-01-01', end='2026-01-10',
                columns=['TradingDay', 'InnerCode', 'close'],
                condition="close > 10")

# Constant table (single Parquet)
rel = LoadConstant('stock', 'stock_info', table_name='StockInfo', columns=['InnerCode', 'name'])
df = rel.df()
```

Paths are built from `DATAROOT`, `category`, and `data_name` (and for constants, `table_name`). Daily data is read only for the requested date range via a list of `YYYYMMDD.parquet` paths.

---

## Adding a new daily dataset

1. In `raw_tushare`, add a new module (or extend an existing one).
2. Subclass `TushareDailyLoader` and call `super().__init__(logger, category, dir_name, data_name, start=..., end=...)`.
3. Implement `_run_func_date_onetime(self, date: str) -> pd.DataFrame` to fetch one day from Tushare and return a DataFrame (e.g. with a `TradingDay` column).
4. Instantiate and run (e.g. from `main.py` or a script). Data will be written under `{DATAROOT}/{category}/{dir_name}/YYYYMMDD.parquet`.
5. Read with `LoadDaily(category, dir_name, start=..., end=...)` (and optional `columns` / `condition`).

---

## Adding a new constant dataset

1. Subclass `TushareConstantLoader` and pass `logger`, `category`, `dir_name`, `data_name`.
2. Implement `_run_func_onetime(self) -> pd.DataFrame`.
3. Run the loader once; it writes a single `{data_name}.parquet` under `{DATAROOT}/{category}/{dir_name}/`.
4. Read with `LoadConstant(category, dir_name, table_name=data_name, ...)`.

---

## Logs

Log files are written under the `logs/` directory (e.g. `logs/stock.log`, `logs/index.log`). Configure the logger in `main.py` or when creating the loader (e.g. `get_logger(..., filename='stock', ifconsole=False)`).

---

## License and attribution

See repository and source file headers for author and license information.
