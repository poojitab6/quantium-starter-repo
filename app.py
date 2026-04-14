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
    "Sales": sales,
    "Date": date,
    "Region": region
})

df['Region'] = df['Region'].str.lower()
df['Sales'] = pd.to_numeric(df['Sales'])
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

df = df.sort_values(by='Date')


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

            dcc.RadioItems(
                id='region-dropdown',
                options = [
                    {'label':'North', 'value':'north'},
                    {'label':'East', 'value':'east'},
                    {'label':'South', 'value':'south'},
                    {'label':'West', 'value':'west'},
                    {'label':'All', 'value':'all'}
                ],
                value='all', #default
                inline=True
            ),

            dcc.Graph(id='line-graph')
        ], className="card")
    ], className="content")

])

@app.callback(
    Output('line-graph', 'figure'),
    Input('region-dropdown', 'value')
)

def update_graph(selected_region):

    return generate_figure(selected_region, df)

def generate_figure(selected_region, df):
    if selected_region == 'all':
        filtered_df = df
        title = "Sales in All Regions"
        color = "Region"
    else:
        filtered_df = df[df['Region'] == selected_region]
        title = f"Sales in {selected_region.capitalize()}"
        color = None

    fig = px.line(
        filtered_df, x="Date", y="Sales", color=color, title=title
    )

    return fig

if __name__== '__main__':
    app.run(debug=True)