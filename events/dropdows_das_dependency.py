import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

terr2 = pd.read_csv('modified_globalterrorismdb_0718dist.csv')

location1 = terr2[['country_txt', 'latitude', 'longitude']]
list_locations = location1.set_index('country_txt')[['latitude', 'longitude']].T.to_dict('dict')

region = terr2['country_txt'].unique()

app = dash.Dash(__name__, )
app.layout = html.Div([



    html.Div([
        html.Div([
            html.P('Select Region:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_countries',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'South Asia',
                         placeholder = 'Select Countries',
                         options = [{'label': c, 'value': c}
                                    for c in region], className = 'dcc_compon'),

            html.P('Select Country:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_countries1',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         placeholder = 'Select Countries',
                         options = [], className = 'dcc_compon'),

            html.P('Select Year:', className = 'fix_label', style = {'color': 'white', 'margin-left': '1%'}),
            dcc.RangeSlider(id = 'select_years',
                            min = 1970,
                            max = 2017,
                            dots = False,
                            value = [2010, 2017]),

        ], className = "create_container three columns"),

        html.Div([
            dcc.Graph(id = 'bar_line_1',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container six columns"),

        html.Div([
            dcc.Graph(id = 'pie',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container three columns"),

    ], className = "row flex-display"),

], id = "mainContainer", style = {"display": "flex", "flex-direction": "column"})


@app.callback(
    Output('w_countries1', 'options'),
    Input('w_countries', 'value'))
def get_country_options(w_countries):
    terr3 = terr2[terr2['region_txt'] == w_countries]
    return [{'label': i, 'value': i} for i in terr3['city'].unique()]


@app.callback(
    Output('w_countries1', 'value'),
    Input('w_countries1', 'options'))
def get_country_value(w_countries1):
    return [k['value'] for k in w_countries1][0]





if __name__ == '__main__':
    app.run_server(debug = True)