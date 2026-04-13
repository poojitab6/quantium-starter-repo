from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import csv
from pathlib import Path
from dash.dependencies import Input, Output

app = Dash()

doc = Path('.\data\output.csv')

sales = []
date = []
region = []

with open(doc, 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        sales.append(row['sales'])
        date.append(row['date'])
        region.append(row['region'])

df = pd.DataFrame({
    "Sales": pd.to_numeric(sales),
    "Date": pd.to_datetime(date),
    "Region": region
})

fig = px.line(df, x="Date", y="Sales", color="Region", labels={"Date": "Date", "Sales": "Sales ($)", "Region": "Region"})

app.layout = html.Div([
    # html.H1("Soul Foods - Pink Morsel Sales", style = {"textAlign": "center"}),
    # dcc.Graph(figure=fig)

    html.Div([
        html.H1("Soul Foods"),
        html.P("Sales Performance")
    ], className="navbar"),

    html.Div([
        html.Div([
            html.H2("Pink Morsel Sales by Region"),

            dcc.Dropdown(
                id='region-dropdown',
                options = [
                    {'label': r, 'value': r}
                    for r in df['Region'].unique()
                ],
                value=df['Region'].unique()[0], #default
                clearable=False
            ),

            dcc.Graph(id='line-graph')
        ], className="card")
    ], className="content")

])

if __name__== '__main__':
    app.run(debug=True)

@app.callback(
    Output('line-graph', 'figure'),
    Input('region-dropdown', 'value')
)

def update_graph(selected_region):
    filtered_df = df[df['Region'] == selected_region]

    fig = px.line(
        filtered_df, x="Date", y="Sales", title=f"Sales in {selected_region}"
    )

    return fig