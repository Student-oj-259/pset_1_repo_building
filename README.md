# pset_1_repo_building

# GDP Analysis — Problem Set 1

A Python project for cleaning, reshaping, and visualising annual GDP data from 2000 to 2022. The analysis is available as a Jupyter notebook and reusable functions in the `fed` package.

## Contents

| File or directory | Purpose |
| --- | --- |
| `GDP_ann.ipynb` | Notebook containing the data preparation and plotting workflow. |
| `fed/data.py` | Functions for loading, cleaning, reshaping, and filtering GDP data. |
| `fed/plot_utils.py` | Function for creating an interactive Plotly chart. |
| `fed/__init__.py` | Exposes the three public functions. |
| `API_Download_DS2_EN_csv_v2_179699.csv` | Included GDP dataset. |
| `requirements.txt` | Python package dependencies. |
| `test.py` | Unit tests for data transformations and chart contents. |

## Setup

Install dependencies from the repository directory:

```bash
python -m pip install -r requirements.txt
```

The dependencies are Polars, Plotly, pandas, and NumPy. Their versions are not pinned.

To use the notebook, also install JupyterLab:

```bash
python -m pip install jupyterlab
```

## Data and transformations

The included CSV contains the indicator `GDP (current US$)` (`NY.GDP.MKTP.CD`) for seven countries over 2000–2022.

The processing functions:

1. Remove country codes, indicator metadata, and the empty trailing column.
2. Convert GDP values into billions of US dollars.
3. Round values to whole billions.
4. Reshape the year columns into a long table with `Country Name`, `Year`, and `GDP`.
5. Filter the table to selected countries.

The default selection is the United States, China, Japan, Germany, and the United Kingdom, producing 115 country-year observations.

Values represent GDP in current US dollars; they are not adjusted for inflation or population.

## Python usage

Run Python from the repository directory so that the local `fed` package and default CSV path can be found.

```python
import fed

gdp = fed.load_and_clean_gdp_data()
gdp_long = fed.get_filtered_long_data(gdp)

fig = fed.plot_gdp_trends(gdp_long)
fig.show()
```

To select different countries:

```python
gdp_long = fed.get_filtered_long_data(
    gdp,
    selected_countries=["Germany", "Japan"],
)

fig = fed.plot_gdp_trends(gdp_long)
fig.show()
```

A custom input path can be passed to `load_and_clean_gdp_data(filepath)`. The input must contain `Country Name` and the year columns `"2000"` through `"2022"`.

Passing an empty country list returns an empty filtered table. Country names must match the dataset.

`plot_gdp_trends()` returns a Plotly figure; displaying or saving it is left to the caller.

## Notebook usage

From the repository directory, run:

```bash
jupyter lab GDP_ann.ipynb
```

Execute the cells in order to load the data, inspect missing values, transform the table, and display the interactive chart.

## Tests

Run the included unittest suite:

```bash
python -m unittest -v test
```

The tests cover cleaned columns, scaling and rounding, long-format values and types, default and custom country selection, empty selections, and chart traces.
