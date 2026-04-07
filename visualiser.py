import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load processed data
df = pd.read_csv("output.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Create app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Dashboard"),

    html.Label("Select Region:"),
    dcc.Dropdown(
        id="region-dropdown",
        options=[{"label": "All", "value": "all"}] +
                [{"label": region.title(), "value": region} for region in sorted(df["Region"].unique())],
        value="all",
        clearable=False
    ),

    dcc.Graph(id="sales-line-chart")
])

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-dropdown", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["Region"] == selected_region]

    # Group sales by date
    sales_by_date = filtered_df.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        sales_by_date,
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time"
    )

    # Add vertical line for price increase date
    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="red"
    )

    fig.add_annotation(
        x="2021-01-15",
        y=sales_by_date["Sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=1
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)