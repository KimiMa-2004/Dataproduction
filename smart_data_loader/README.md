# SmartDataLoader

A small utility library for logging and data visualization (e.g. time series, scatter, histograms, correlation heatmaps, subplot grids). Use it by placing the `smart_dataloader` folder in your project and importing from it.

---

## Project setup

### 1. Add the package to your project

Copy the `smart_dataloader` folder into your project so you can import it:

```text
your_project/
  smart_dataloader/
    __init__.py
    logger/
    visualization/
    ...
  ...
  .env
```

### 2. Dependencies

Install the required packages (e.g. in a virtualenv):

```bash
pip install pandas numpy matplotlib seaborn python-dotenv
```

### 3. Environment (optional)

Create a `.env` in the project root if you want to override defaults:

```env
# Logger: level (DEBUG, INFO, WARNING, ERROR) and directory for log files
LOG_LEVEL=INFO
LOGGER_DIR=./logs
```

The library uses `python-dotenv` and will load `.env` when the logger module is first used. If `LOGGER_DIR` is not set, logs are written under `./logs` by default.

---

## Logger

Log to console and/or to a file. Log level and file directory can be set via environment variables above.

### `get_logger`

Returns a configured logger. You can use it with only console output, or also write to a file.

```python
from smart_dataloader.logger import get_logger

# Console only, default name and level from LOG_LEVEL
logger = get_logger()
logger.info("Application started")
logger.warning("Something to check")

# Also write to file ./logs/my_app.log (LOGGER_DIR/filename.log)
logger = get_logger(name="my_app", filename="my_app", ifconsole=True)
logger.info("This goes to console and to ./logs/my_app.log")

# File only, no console; custom level
logger = get_logger(name="batch", filename="batch", ifconsole=False, level="DEBUG")
logger.debug("Debug message only in file")
```

**Parameters:**

| Parameter   | Description |
|------------|-------------|
| `name`     | Logger name (default `"smart_dataloader"`). |
| `filename` | If set, log to `{LOGGER_DIR}/{filename}.log`. `None` = no file. |
| `level`    | Log level, e.g. `"DEBUG"`, `"INFO"`. Uses env `LOG_LEVEL` if `None`. |
| `ifconsole`| If `True`, also print to console (default `True`). |

### `delete_logger_file`

Removes a log file by logger name and closes its file handler (so it works on Windows when the file was in use).

```python
from smart_dataloader.logger import get_logger, delete_logger_file

logger = get_logger(filename="temp_job")
logger.info("Done")
# When you no longer need the file (e.g. after tests):
delete_logger_file("temp_job")  # Deletes ./logs/temp_job.log
```

**Parameter:** `filename` — same name you passed to `get_logger` as `filename` (default `"smart_dataloader"`).

---

## Visualization

All plot classes share common options: `figsize`, `imgpath`, `title`, `xlabel`, `ylabel`, `grid`, `legend`, `logger`. If `imgpath` is set, the figure is saved and the figure window is closed; otherwise `plt.show()` is used.

### `TimeSeriesPlot`

Multiple time series (or x–y lines) on one figure.

```python
from smart_dataloader.visualization import TimeSeriesPlot

# Each of xs, ys, labels: one series. Lengths must match.
xs = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
ys = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
labels = ["Series A", "Series B"]

ts = TimeSeriesPlot(
    xs, ys, labels,
    title="My time series",
    xlabel="Time",
    ylabel="Value",
    imgpath="timeseries.png",
)
ts.draw()
```

Optional: `widths` (line widths), `markers` (marker styles) per series, same length as `labels`.

### `ScatterPlot`

Multiple scatter series on one figure (e.g. several (x, y) datasets with labels).

```python
from smart_dataloader.visualization import ScatterPlot

xs = [[1, 2, 3], [2, 3, 4]]
ys = [[2, 4, 5], [1, 3, 2]]
labels = ["Group 1", "Group 2"]

sc = ScatterPlot(xs, ys, labels, title="Scatter", imgpath="scatter.png")
sc.draw()
```

Optional: `sizes`, `markers` per series.

### `HistPlot`

Single-column histogram with optional KDE density curve.

```python
from smart_dataloader.visualization import HistPlot
import numpy as np

data = np.random.randn(500)

# Histogram only
h = HistPlot(data, bins=30, title="Distribution", imgpath="hist.png")
h.draw()

# Histogram + density curve (KDE)
h = HistPlot(
    data,
    bins=20,
    density_curve=True,
    title="Distribution",
    xlabel="Value",
    ylabel="Density",
    imgpath="hist_kde.png",
)
h.draw()
```

**Parameters:** `data` (1-d array-like), `bins` (int or `None` for auto), `density_curve` (bool).

### `plot_correlation_heatmap`

Correlation matrix as a heatmap. Input can be a DataFrame or a list of 1-d arrays (one variable per array).

```python
from smart_dataloader.visualization import plot_correlation_heatmap
import pandas as pd
import numpy as np

# From DataFrame: use all numeric columns or specify columns
df = pd.DataFrame({"a": [1, 2, 3], "b": [2, 4, 5], "c": [0, 1, 0]})
plot_correlation_heatmap(df, imgpath="corr_df.png")
plot_correlation_heatmap(df, columns=["a", "b"], imgpath="corr_ab.png")

# From list of arrays (one variable per array)
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([2, 4, 5, 4, 5])
arr3 = np.array([0, 1, 0, 1, 0])
plot_correlation_heatmap(
    [arr1, arr2, arr3],
    columns=["x", "y", "z"],
    title="Correlation",
    imgpath="corr_arrays.png",
)
```

Optional: `figsize`, `title`, `annot`, `fmt`, `cmap`, `vmin`, `vmax`, `logger`.

### `plot_pair_grid`

Pair plot: diagonal = distribution of each variable, off-diagonal = scatter of variable i vs j.

```python
from smart_dataloader.visualization import plot_pair_grid
import numpy as np

arr1 = np.random.randn(100)
arr2 = np.random.randn(100)
arr3 = np.random.randn(100)

plot_pair_grid(
    [arr1, arr2, arr3],
    columns=["A", "B", "C"],
    diag_kind="kde",   # or "hist"
    title="Pair plot",
    imgpath="pair_grid.png",
)
```

**Parameters:** `data` (DataFrame or list of 1-d arrays), `columns` (optional labels), `diag_kind` (`"hist"` or `"kde"`), `figsize`, `title`, `imgpath`, `alpha`, `logger`.

### `plot_subplots`

One figure with multiple panels. Each panel is drawn by an existing plot instance (`TimeSeriesPlot`, `ScatterPlot`, or `HistPlot`). You pass a list of these instances; their data and per-panel options (title, xlabel, ylabel, etc.) are used, while `imgpath` and `figsize` on each instance are ignored. Layout and whole-figure options are set in `plot_subplots`.

```python
from smart_dataloader.visualization import (
    TimeSeriesPlot,
    ScatterPlot,
    HistPlot,
    plot_subplots,
)
import numpy as np

xs = [[0, 1, 2, 3, 4]] * 2
ys = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
labels = ["A", "B"]

ts = TimeSeriesPlot(xs, ys, labels, title="Time Series")
sc = ScatterPlot(xs, ys, labels, title="Scatter")
hs = HistPlot(np.random.randn(100), title="Histogram", bins=15, density_curve=True)

# One figure, 3 panels; default 2 columns => 2 rows
plot_subplots(
    [ts, sc, hs],
    title="Overview",
    ncols=2,
    imgpath="subplots.png",
)

# Fixed grid (e.g. 1 row, 3 columns)
plot_subplots(
    [ts, sc, hs],
    size=(1, 3),
    title="Overview",
    imgpath="subplots_1x3.png",
)
```

**Parameters:**

| Parameter  | Description |
|-----------|-------------|
| `plotters` | List of `TimeSeriesPlot` / `ScatterPlot` / `HistPlot` instances. |
| `size`     | Optional `(nrows, ncols)`. If omitted, layout is inferred from `ncols`. |
| `ncols`    | Number of columns when `size` is not set (default `2`). |
| `figsize`  | Total figure (width, height). Default depends on grid size. |
| `title`    | Main figure title (suptitle). |
| `imgpath`  | Save the whole figure to this path; `None` = show. |
| `logger`   | Optional logger for save message. |

---

## Minimal example

```python
from smart_dataloader.logger import get_logger
from smart_dataloader.visualization import HistPlot, plot_correlation_heatmap
import numpy as np

logger = get_logger(filename="demo")
logger.info("Start")

data = np.random.randn(200)
HistPlot(data, bins=20, density_curve=True, title="Demo", imgpath="demo_hist.png").draw()

plot_correlation_heatmap(
    [data, np.random.randn(200), np.random.randn(200)],
    columns=["X", "Y", "Z"],
    imgpath="demo_corr.png",
)

logger.info("Done")
```

This uses the logger (console + file if `filename` is set), a single histogram with KDE, and a correlation heatmap from three arrays, with minimal configuration.

---

## Future updates (roadmap)

Planned modules and features:

- **High-performance I/O for financial data**  
  Fast read/write for market data (e.g. tick, OHLCV), using DuckDB or similar for columnar storage and SQL-style queries.

- **Preprocessing for financial data and ML**  
  Common pipelines: normalization, returns, technical indicators, train/val/test splits, handling missing values and outliers in financial time series.

- **Generic ML models and training utilities**  
  Reusable model wrappers and training loops (e.g. sklearn-style fit/predict), basic hyperparameter and evaluation helpers, suitable for quick experiments on tabular/time-series data.