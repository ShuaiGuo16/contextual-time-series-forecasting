# Let Decision Models Improve Your Time Series Forecasts

A hands-on tutorial pairing **Jev** with the **Chronos-2 time series foundation model** to turn unstructured operational records into forecasting covariates.

**Operational records → Jev interpretation → numerical covariates → Chronos-2 forecast**

Start with the [executed notebook](contextual_time_series_forecasting.ipynb).

## The example

We forecast an office building's hourly electricity consumption using eight weeks of history and plans for the following week. The readings and records are synthetic examples prepared for this tutorial.

Jev reads the building policy and operational records to select two features: occupied-zone count and ventilation state. Chronos-2 receives their historical and future values alongside historical consumption. We compare its forecast with one using consumption history alone.

![Forecast comparison](results/forecast_comparison.png)

| Forecast | Whole-week MAE (kWh) | Whole-week RMSE (kWh) |
|---|---:|---:|
| Without contextual covariates | 3.23 | 9.50 |
| With Jev-derived covariates | 0.99 | 1.46 |

See [RESULTS.md](RESULTS.md) for the interpreted events, numerical results, and model revision used in the recorded run.

## Run the tutorial

Use Python 3.12 and create an environment. The following commands use Windows paths:

```powershell
py -3.12 -m venv .venv
```

For an NVIDIA GPU, install a compatible CUDA build of PyTorch first. The recorded run used this build:

```powershell
.venv\Scripts\python -m pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cu128
```

Then install the remaining requirements. For CPU execution, proceed directly to this step after creating the environment:

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
```

Copy [.env.example](.env.example) to `.env` and set `OPENROUTER_API_KEY`. Open the notebook, select the `.venv` interpreter, and run its cells in order.

Chronos-2 runs locally and loads the pinned pretrained weights from Hugging Face. Jev requests go to OpenRouter's native Decisions API and incur API charges. The saved outputs can be inspected without rerunning either model.

## Data

- [electricity.csv](data/electricity.csv): 1,512 hourly readings, including 1,344 historical hours and 168 forecast hours.
- [building_context.txt](data/building_context.txt): building layout and standing operating policy.
- [operational_records.json](data/operational_records.json): dated calendar entries, emails, and facilities notes grouped by applicable date.
- [make_fixture.py](data/make_fixture.py): optional generator for the synthetic meter readings. The notebook does not read its authored operating states.

The tutorial uses predefined assessment intervals and assigns each pair of Jev choices to the corresponding hourly rows. The synthetic plans align with those intervals. The same feature questions are used throughout the historical and future periods.

Both forecasts use the same historical consumption, model revision, and horizon. Future consumption is used only to evaluate the predictions. Jev's requests contain building facts and records, with no meter readings or expected feature values.

## Saved outputs

- [Example Jev request](results/jev_request_evening_seminar.json) and [native requests and responses](results/feature_decisions.json).
- [Hourly covariates](results/interpreted_covariates.csv) and [future covariates](results/future_covariates.csv).
- [Forecast comparison](results/forecast_comparison.csv), [whole-week metrics](results/metrics.csv), and [event results](results/event_results.csv).
- [Run configuration and provenance](results/run_summary.json).
- PNG figures and editable SVG versions in [results](results/), covering the pipeline, historical timeline, covariates, and forecasts.
