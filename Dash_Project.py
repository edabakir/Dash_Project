from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import json
from urllib.request import urlopen
import pandas as pd

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response1:
    counties = json.load(response1)

url1 = 'https://raw.githubusercontent.com/edabakir/Dash_Project/main/United_States_COVID-19_Community_Levels_by_County%20.csv'
df1 = pd.read_csv(url1, dtype={"fips": str})

url2 = 'https://raw.githubusercontent.com/edabakir/Dash_Project/main/PovertyEstimates%20(1).csv'
df2 = pd.read_csv(url2, dtype={"fips": str})


def pad(aFIPS):
    if len(aFIPS) == 5:
        return aFIPS
    else:
        return "0" + aFIPS

df1['fips'] = df1['fips'].apply(str).apply(pad)
df2['FIPS_code'] = df2['FIPS_code'].apply(str).apply(pad)

app = Dash(__name__, suppress_callback_exceptions=True)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('U.S. COVID DASHBOARD', href='/page-1'),
    html.Br(),
    dcc.Link('U.S. POVERTY DASHBOARD', href='/page-2'),
])

dropdown_names = ['Covid inpatient bed utilization','Covid hospital admissions per 100k', 'Covid cases per 100k']

page_1_layout = html.Div([
    html.H4('COVID METRICS BY COUNTY'),
    dcc.Dropdown(
        id='fig_dropdown1',
        options=[{'label': x, 'value': x} for x in dropdown_names],
        value="Covid cases per 100k"),
    dcc.Graph(id = 'graph1'),
    html.Br(),
    dcc.Link('U.S. POVERTY DASHBOARD', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@callback(
    Output('graph1', 'figure'),
    [Input('fig_dropdown1', 'value')])

def display_choropleth1(fig_dropdown1):
    fig1 = px.choropleth(df1, geojson=counties,
                            locations='fips',
                            color= fig_dropdown1,
                            color_continuous_scale="rdylgn_r",
                            range_color=(0, 150),
                            scope="usa",
                            hover_name='county')

    return fig1

dropdown_names_2 = ['Total Poverty', 'Childhood Poverty (0-17)', 'Childhood Poverty (5-17)']

page_2_layout = html.Div([
    html.H1('U.S. POVERTY RATES BY COUNTY'),
    dcc.Dropdown(
        id='fig_dropdown2',
        options=[{'label': x, 'value': x} for x in dropdown_names_2],
        value="Total Poverty"),
    dcc.Graph(id = 'graph2'),
    html.Br(),
    dcc.Link('U.S. COVID DASHBOARD', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@callback(
    Output('graph2', 'figure'),
    [Input('fig_dropdown2', 'value')])

def display_choropleth(fig_dropdown2):
    fig2 = px.choropleth(df2, geojson=counties,
                            locations='FIPS_code',
                            color= fig_dropdown2,
                            color_continuous_scale="rdylgn_r",
                            range_color=(0, 25),
                            scope="usa",
                            hover_name='Area_name')

    return fig2


# Update the index
@callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)