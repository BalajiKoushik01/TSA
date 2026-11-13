# Onion-price time-series analysis

An academic time-series project analysing historical onion-price data with seasonal decomposition, smoothing, model diagnostics and forecasting visualisations.

**Context:** coursework at Christ University. The repository contains code and an interactive HTML presentation; it is not a live commodity-pricing service.

## Files in this repository

- `data/onion_monthly.csv` — historical input dataset.
- `scripts/onion_analysis.py` — Python analysis and plotting script.
- `visualizations/` — saved figures.
- `FINAL_WORKING_PRESENTATION.html` — browser-based project presentation.

The earlier README referenced a research-paper file that is **not present** in the tracked repository. The updated documentation does not link to it.

## Run the analysis

The analysis script resolves input and output paths from its own location, so it can be run from the repository root or another working directory.

```bash
git clone https://github.com/BalajiKoushik01/TSA.git
cd TSA
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install pandas numpy matplotlib seaborn statsmodels scipy
python scripts/onion_analysis.py
```

Open `FINAL_WORKING_PRESENTATION.html` in a modern browser to read the presentation. Note that regenerating outputs may overwrite existing charts.

## Interpretation

The plotted forecast and diagnostics describe the historical dataset and modelling choices. Forecasts, confidence bounds and seasonal patterns are **not** guarantees of future onion prices. To reproduce a reported number, verify the data range, train/test split, fitted model, forecast date and diagnostic results.

No claim is made here that the model remains accurate on current market data.

## Genuine forecast-error validation

The `19_rolling_rmse.png` chart uses an **observed expanding-window seasonal-naive baseline**, evaluated one month ahead at each available month after at least 24 months of history. Each prediction uses only the price 12 months earlier; its cumulative RMSE is calculated from observed forecast errors. Unlike the previous plot, it contains **no synthetic or randomly generated accuracy trend**. This assesses a transparent baseline, not the SARIMA/other fitted model shown elsewhere. It does not prove the fitted model generalizes. Regression tests: `python -m unittest discover -s tests -v`.
