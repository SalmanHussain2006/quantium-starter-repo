import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("output.csv")

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# Create Dash app
app = Dash(__name__)
app.title = "Soul Foods Dashboard"

app.layout = html.Div(
    className="main-container",
    children=[
        html.Div(
            className="card",
            children=[
                html.H1("Soul Foods Pink Morsel Sales", className="title"),
                html.P(
                    "Track sales over time and filter by region to compare performance before and after the price increase on 15 January 2021.",
                    className="subtitle",
                ),

                html.Div(
                    className="radio-container",
                    children=[
                        html.Label("Select Region", className="radio-label"),
                        dcc.RadioItems(
                            id="region-radio",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            className="radio-items",
                            labelClassName="radio-option",
                        ),
                    ],
                ),

                dcc.Graph(id="sales-chart", className="graph"),
            ],
        )
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-radio", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.copy()
        chart_title = "Pink Morsel Sales Across All Regions"
    else:
        filtered_df = df[df["Region"].str.lower() == selected_region]
        chart_title = f"Pink Morsel Sales in {selected_region.title()} Region"

    sales_by_date = filtered_df.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        sales_by_date,
        x="Date",
        y="Sales",
        title=chart_title,
        markers=True,
    )

    fig.add_vline(
        x=pd.to_datetime("2021-01-15"),
        line_dash="dash",
        line_color="red",
        annotation_text="Price Increase",
        annotation_position="top right",
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=14),
        margin=dict(l=40, r=40, t=70, b=40),
    )

    fig.update_traces(line=dict(width=3))

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB")

    return fig


if __name__ == "__main__":
    app.run(debug=True)