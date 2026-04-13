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

fig = px.line(df, x="Date", y="Sales", color="Region", title = "Pink Morsel Sales Over Time")

app.layout = html.Div([
    html.H1("Soul Foods - Pink Morsel Sales", style = {"textAlign": "center"}),
    dcc.Graph(figure=fig)
], style = {"fontFamily": "Arial, Helvetica, Verdana"})

if __name__== '__main__':
    app.run(debug=True)