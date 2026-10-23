from pathlib import Path
import unittest

import polars as pl

import fed


CSV = Path(__file__).resolve().parent / "API_Download_DS2_EN_csv_v2_179699.csv"


class TestGDP(unittest.TestCase):
    def test_shape_and_columns(self):
        GDP_Ann_df = fed.load_and_clean_gdp_data(CSV)
        year_columns = [str(year) for year in range(2000, 2023)]
        self.assertEqual(GDP_Ann_df.columns, ["Country Name", *year_columns])
        self.assertGreater(GDP_Ann_df.height, 0)

    def test_scaling_to_billions(self):
        GDP_Ann_df = fed.load_and_clean_gdp_data(CSV)
        GDP_Ann_df_raw = pl.read_csv(CSV)
        year_columns = [str(year) for year in range(2000, 2023)]
        for col in year_columns:
            with self.subTest(year=col):
                self.assertEqual(
                    GDP_Ann_df[col].to_list(),
                    (GDP_Ann_df_raw[col] / 1e9).round().to_list(),
                )

    def test_long_format(self):
        GDP_Ann_df = fed.load_and_clean_gdp_data(CSV)
        GDP_Ann_df_filtered = fed.get_filtered_long_data(GDP_Ann_df)
        selected_countries = [
            "United States", "China", "Japan", "Germany", "United Kingdom"
        ]
        self.assertEqual(GDP_Ann_df_filtered.columns, ["Country Name", "Year", "GDP"])
        self.assertEqual(
            set(GDP_Ann_df_filtered["Country Name"]), set(selected_countries)
        )
        self.assertEqual(GDP_Ann_df_filtered.height, 115)
        self.assertEqual(GDP_Ann_df_filtered["Year"].dtype, pl.Int32)
        self.assertEqual(set(GDP_Ann_df_filtered["Year"]), set(range(2000, 2023)))
        self.assertEqual(GDP_Ann_df_filtered["GDP"].null_count(), 0)
        for country in selected_countries:
            with self.subTest(country=country):
                GDP_Ann_df_long = GDP_Ann_df_filtered.filter(
                    pl.col("Country Name") == country
                ).sort("Year")
                self.assertEqual(
                    tuple(GDP_Ann_df_long["GDP"]),
                    GDP_Ann_df.filter(pl.col("Country Name") == country)
                    .select([str(year) for year in range(2000, 2023)])
                    .row(0),
                )

    def test_custom_country_filter(self):
        GDP_Ann_df = fed.load_and_clean_gdp_data(CSV)
        selected_countries = ["Germany", "Japan"]
        GDP_Ann_df_filtered = fed.get_filtered_long_data(
            GDP_Ann_df, selected_countries=selected_countries
        )
        self.assertEqual(
            set(GDP_Ann_df_filtered["Country Name"]), set(selected_countries)
        )
        self.assertEqual(GDP_Ann_df_filtered.height, 46)

    def test_empty_country_filter(self):
        GDP_Ann_df = fed.load_and_clean_gdp_data(CSV)
        GDP_Ann_df_filtered = fed.get_filtered_long_data(
            GDP_Ann_df, selected_countries=[]
        )
        self.assertEqual(GDP_Ann_df_filtered.height, 0)

    def test_plot_has_one_trace_per_country(self):
        GDP_Ann_df = fed.load_and_clean_gdp_data(CSV)
        GDP_Ann_df_filtered = fed.get_filtered_long_data(GDP_Ann_df)
        fig = fed.plot_gdp_trends(GDP_Ann_df_filtered)
        self.assertEqual(len(fig.data), 5)
        self.assertEqual(
            {trace.name for trace in fig.data},
            set(GDP_Ann_df_filtered["Country Name"]),
        )
        for trace in fig.data:
            with self.subTest(country=trace.name):
                GDP_Ann_df_long = GDP_Ann_df_filtered.filter(
                    pl.col("Country Name") == trace.name
                )
                self.assertEqual(list(trace.x), GDP_Ann_df_long["Year"].to_list())
                self.assertEqual(list(trace.y), GDP_Ann_df_long["GDP"].to_list())


if __name__ == "__main__":
    unittest.main()
