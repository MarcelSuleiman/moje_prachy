import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from django_plotly_dash import DjangoDash
import dash
import sqlite3
import pandas as pd

'''
connection = sqlite3.connect('.\\db.sqlite3')

query = "SELECT * FROM events_items WHERE owner = '{}'".format('Iveta')

df = pd.read_sql_query(query, connection)
df = df.sort_values(by='date_of_purchase_time_stamp', ascending=True)

connection.close()

app = DjangoDash('SimpleExample')

app.layout = html.Div([
html.H1('Graf jednotlivé kategórie - detail'),

dcc.Dropdown(id='choice',
            options=[{'label':x, 'value':x} for x in sorted(df.category_id.unique())],
            value='Potraviny'),

dcc.Graph(id='my-graph', figure={})

])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='choice', component_property='value')
    )

#def interactive_graphing(value):
def display_value(value):
    print(value)
    dff = df[df.item_class == value]
    fig = px.pie(data_frame=dff, names='item_sub_class', values='price_per_all')
    return fig
'''
#return render(request, 'events/dash_interactive.html')
#return {'data': [fig], 'layout': layout}

'''

app = DjangoDash('SimpleExample')   # replaces dash.Dash

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value='red'
    ),
    html.Div(id='output-color'),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i,
                  'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        value='medium'
    ),
    html.Div(id='output-size')

])

@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value

@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                  dropdown_color)

'''



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1('Niečo sa pokazilo, tak aspoň graf so sliderom'),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ),
])


@app.callback(
               Output('slider-graph', 'figure'),
              [Input('slider-updatemode', 'value')])
def display_value(value):


    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i*i)

    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),

    )
    return {'data': [graph], 'layout': layout}
