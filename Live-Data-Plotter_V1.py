# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 08:33:30 2020

@author: evan.kias
"""

import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go 
# import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Real-Time Data Viewer'),
        #html.Div(id='live-update-text'),
        
        html.Label('File Path:'),
            dcc.Input(id='full-filepath', value='', type='text', style={
            'width': '100%',
            }),
            
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5000,  # in milliseconds
            n_intervals=0
            ),
        dcc.RadioItems(
            id='Num-Transducers',
            options=[
                {'label': '1 Transducer', 'value': '1'},
                {'label': '2 Transducers', 'value': '2'}
            ],
            value='2',
            labelStyle={'display': 'inline-block'}
                       )
            ])
)


@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals'),
               Input('full-filepath','value'),
               Input('Num-Transducers', 'value')]
             )
def liveupdate(n,filepath_,numTs):
    print(filepath_)
    if filepath_:
        df_dxd = pd.read_csv(filepath_)
        df_dxd = pd.read_csv(filepath_, skiprows=7, error_bad_lines=False)
        if numTs == '2':
            df_dxd.drop(df_dxd.columns[[3, 4, 6,7]], axis=1, inplace=True)
            df_dxd.columns = ['Date', 'Time', 'Outlet', 'Inlet']
            df_dxd['DateTime'] = pd.to_datetime(df_dxd['Date'] + " " + df_dxd['Time'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_dxd.DateTime, y=df_dxd.Outlet,
                                 name="Outlet"))
            fig.add_trace(go.Scatter(x=df_dxd.DateTime, y=df_dxd.Inlet,
                                name="Inlet", yaxis = "y2"))
            # Set y-axes titles
            fig.update_layout(yaxis=dict(title="Outlet", titlefont=dict(color="#1f77b4"), 
                                         tickfont=dict(color="#1f77b4")),
                               yaxis2=dict(title="Inlet",titlefont=dict(
                                   color="#ff7f0e"), tickfont=dict(color="#ff7f0e"),
                                   anchor="x", overlaying="y", side="right"),
                               uirevision='foo'
                               )
        if numTs == '1':
            df_dxd.drop(df_dxd.columns[[3]], axis=1, inplace=True)
            df_dxd.columns = ['Date', 'Time', 'Pressure']
            df_dxd['DateTime'] = pd.to_datetime(df_dxd['Date'] + " " + df_dxd['Time'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_dxd.DateTime, y=df_dxd.Pressure,
                                 name="Pressure"))
            # Set y-axes titles
            fig.update_layout(yaxis=dict(title="Pressure", titlefont=dict(color="#1f77b4"), 
                                         tickfont=dict(color="#1f77b4")),
                               uirevision='foo'
                               )                           
        return fig
    else:
        # fig = px.scatter(x=[1], y=[1])
        fig = go.Figure(go.Scatter(x=[1], y=[1], mode='markers'))
        return fig

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=True,port=8105,host='10.0.100.140')