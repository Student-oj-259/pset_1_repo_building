# fed/plot_utils.py
import plotly.express as px

def plot_gdp_trends(GDP_Ann_df_filtered):
    fig = px.line(
        GDP_Ann_df_filtered, 
        x="Year", 
        y="GDP", 
        color="Country Name", 
        markers=True, 
        title="GDP over time (2000 - 2022) across Wealthy Countries", 
        labels={"GDP": "GDP (Billions USD)", "Year": "Year", "Country Name": "Country"})
    
    return fig