from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import csv
from pathlib import Path

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
    "Sales": sales,
    "Date": date,
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
            dcc.Graph(figure=fig)
        ], className="card")
    ], className="content")

])

if __name__== '__main__':
    app.run(debug=True)