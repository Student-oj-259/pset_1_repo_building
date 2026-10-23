# fed/data.py
import polars as pl


def load_and_clean_gdp_data(filepath: str = "API_Download_DS2_EN_csv_v2_179699.csv") -> pl.DataFrame:
    pl.Config.set_tbl_hide_column_data_types(True)
    GDP_Ann_df = pl.read_csv(filepath)
    
    # Drop unwanted columns safely
    GDP_Ann_df = GDP_Ann_df.drop(["Country Code", "Indicator Name", "Indicator Code", ""], strict=False)
    
    # Scale year columns to billions and round
    year_columns = [str(year) for year in range(2000, 2023)]
    GDP_Ann_df = GDP_Ann_df.with_columns([pl.col(col) / 1e9 for col in year_columns])
    GDP_Ann_df = GDP_Ann_df.with_columns([pl.col(col).round() for col in year_columns])
    
    return GDP_Ann_df

def get_filtered_long_data(GDP_Ann_df: pl.DataFrame, selected_countries: list = None) -> pl.DataFrame:
    """Melts the wide DataFrame into long format and filters for selected countries."""
    if selected_countries is None:
        selected_countries = ["United States", "China", "Japan", "Germany", "United Kingdom"]
        
    year_columns = [str(year) for year in range(2000, 2023)]
    
    GDP_Ann_df_long = GDP_Ann_df.unpivot(
        index=["Country Name"],
        on=year_columns,
        variable_name="Year",
        value_name="GDP"
    )
    
    GDP_Ann_df_long = GDP_Ann_df_long.with_columns(pl.col("Year").cast(pl.Int32))
    GDP_Ann_df_filtered = GDP_Ann_df_long.filter(pl.col("Country Name").is_in(selected_countries))
    
    return GDP_Ann_df_filtered