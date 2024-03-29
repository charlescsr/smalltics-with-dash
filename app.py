import base64
import io

import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.H1(children='Smalltics Dashboard', style={'text-align': 'center'}), html.Br(),
    html.H3(children='Upload your dataset and select the axes and plot and voila', style={'text-align': 'center'}),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        style={
            'width': '99%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='output-plot')
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            
            if any(df.columns.str.contains('^Unnamed')):
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')), index_col=0)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename), 

        dash_table.DataTable(
            data=df.head().to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns], id='dataset',
        ),
        html.Div(id='secret-df', hidden=True, children=df.to_json(orient='split')),

        html.Hr(),  # horizontal line
        dcc.Dropdown(
        id='x_axis',
        options=[
            {'label': i, 'value': i} for i in df.columns
        ],
        clearable=False,
        ),
        html.Br(), html.Br(),
        dcc.Dropdown(
        id='y_axis',
        options=[
            {'label': i, 'value': i} for i in df.columns
        ],
        clearable=False,
        ),

        html.Br(), html.Br(),
        dcc.Dropdown(
        id='plot_type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Plot', 'value': 'line'},
            {'label': 'Bar Plot', 'value': 'bar'},
            {'label': 'Sunburst Plot', 'value': 'sunburst'},
            {'label': 'Treemap Plot', 'value': 'treemap'},
            {'label': 'Pie Chart', 'value': 'pie'}
        ],
        clearable=False,
        )
        # For debugging, display the raw contents provided by the web browser
        #html.Div('Raw Content'),
        #html.Pre(contents[0:200] + '...', style={
        #    'whiteSpace': 'pre-wrap',
        #    'wordBreak': 'break-all'
        #})
    ], id='plot-div')


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names)]
        return children

@app.callback(Output('output-plot', 'children'),
                Input('x_axis', 'value'), Input('y_axis', 'value'), 
                Input('plot_type', 'value'), Input('secret-df', 'children'))
def return_plot(x_axis, y_axis, plot_type, dataset):
    df = pd.read_json(dataset, orient='split')
    
    if plot_type == 'scatter':

        return html.Div([dcc.Graph(
                id='scatter-plot',
                figure={
                    'data': [
                        go.Scatter(
                            x=df[x_axis],
                            y=df[y_axis],
                            mode='markers',
                            marker={
                                'size': 10,
                                'opacity': 0.7,
                                'line': {'width': 0.5, 'color': 'white'}
                            }
                        )
                    ],
                    'layout': go.Layout(
                        xaxis={'title': x_axis},
                        yaxis={'title': y_axis},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )])
    
    elif plot_type == 'line':
        
        return html.Div([dcc.Graph(
                id='line-plot',
                figure={
                    'data': [
                        go.Scatter(
                            x=df[x_axis],
                            y=df[y_axis],
                            mode='lines',
                            line={
                                'shape': 'spline',
                                'width': 3
                            }
                        )
                    ],
                    'layout': go.Layout(
                        xaxis={'title': x_axis},
                        yaxis={'title': y_axis},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )])

    elif plot_type == 'bar':
        
        return html.Div([dcc.Graph(
                id='bar-plot',
                figure={
                    'data': [
                        go.Bar(
                            x=df[x_axis],
                            y=df[y_axis],
                            marker={
                                'color': '#7FDBFF'
                            }
                        )
                    ],
                    'layout': go.Layout(
                        xaxis={'title': x_axis},
                        yaxis={'title': y_axis},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )])

    elif plot_type == 'sunburst':
        
        return html.Div([dcc.Graph(
                id='sunburst-plot',
                figure={
                    'data': [
                        go.Sunburst(
                            labels=df[x_axis],
                            values=df[y_axis],
                            marker={
                                'color': '#7FDBFF'
                            }
                        )
                    ],
                    'layout': go.Layout(
                        xaxis={'title': x_axis},
                        yaxis={'title': y_axis},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )])

    elif plot_type == 'treemap':
        
        return html.Div([dcc.Graph(
                id='treemap-plot',
                figure={
                    'data': [
                        go.Treemap(
                            labels=df[x_axis],
                            values=df[y_axis],
                            marker={
                                'color': '#7FDBFF'
                            }
                        )
                    ],
                    'layout': go.Layout(
                        xaxis={'title': x_axis},
                        yaxis={'title': y_axis},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )])

    elif plot_type == 'pie':

        return html.Div([dcc.Graph(
                id='pie-plot',
                figure={
                    'data': [
                        go.Pie(
                            labels=df[x_axis],
                            values=df[y_axis],
                            marker={
                                'colors': ['#7FDBFF', '#0074D9', '#FF4136', '#2ECC40', '#FF851B', '#B10DC9', '#FFDC00', '#001f3f', '#39CCCC', '#01FF70', '#85144b', '#F012BE', '#3D9970', '#111111', '#AAAAAA']
                            }
                        )
                    ],
                    'layout': go.Layout(
                        xaxis={'title': x_axis},
                        yaxis={'title': y_axis},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )])

if __name__ == '__main__':
    app.run_server()