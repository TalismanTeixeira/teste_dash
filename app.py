import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template('minty')
app =dash.Dash(external_stylesheets=[dbc.themes.MINTY])
server=app.server


df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])



# =========  Layout  =========== #
app.layout = html.Div(children=[
        dbc.Row([
            dbc.Col([
                    dbc.Card([
                        html.H2('ASIMOV', style={'font-family': 'Voltaire','font-size': '30px'}),
                        html.Hr(),
                        html.H5('Cidades:'),
                        dcc.Checklist(df_data['City'].value_counts().index,
                            df_data['City'].value_counts().index,
                            id = 'check-city',
                            inputStyle={'margin-right':'5px','margin-left':'20px'}),
                        html.H5('Variável de análise:', style={'margin-top':'50px'}),
                        dcc.RadioItems(['gross income','Rating'],'gross income',
                            id = 'main-variable',
                            inputStyle={'margin-right':'5px','margin-left':'20px'}),
                    ], style={'height':'150vh','margin':'20px','padding':'20px'})
                    
            ],lg=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col([dcc.Graph(id='city-fig')],sm=4),
                    dbc.Col([dcc.Graph(id='gender-fig')],sm=4),
                    dbc.Col([dcc.Graph(id='pay-fig')],sm=4),
                ]),
                dbc.Row([dcc.Graph(id='income-per-date-fig')]),
                dbc.Row([dcc.Graph(id='income-per-product-fig')]),
            ], lg=9),
        ]),
    ])


# =========  Callbacks  =========== #
@app.callback([Output('city-fig','figure'),
               Output('pay-fig','figure'),
               Output('gender-fig','figure'),
               Output('income-per-date-fig','figure'),
               Output('income-per-product-fig','figure')
               ],
        
               [Input('check-city','value'),
                Input('main-variable','value')])

def render_graphs(cities,main_variable):
    operation = np.sum if main_variable =='gross income' else np.mean
    df_filtered = df_data[df_data['City'].isin(cities)]
    df_city = df_filtered.groupby('City')[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(['Gender', 'City'])[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby('Payment')[main_variable].apply(operation).to_frame().reset_index()
    df_income_time = df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(['Product line','City'])[main_variable].apply(operation).to_frame().reset_index()
        
    fig_city = px.bar(df_city,x='City',y=main_variable)
    fig_payment = px.bar(df_payment,y='Payment',x=main_variable, orientation='h')
    fig_gender = px.bar(df_gender,x='Gender',y=main_variable, color='City', barmode='group')
    fig_income_date = px.bar(df_income_time,x='Date',y=main_variable)
    fig_product_income = px.bar(df_product_income,y='Product line',x=main_variable, barmode='group', color='City', orientation='h')
    
    for fig in [fig_city,fig_payment,fig_gender,fig_income_date]:
        fig.update_layout(margin = dict(l=0, r=0, t=20, b=20), height  = 200, template='minty')    
    

    fig_product_income.update_layout(margin = dict(l=0, r=0, t=20, b=20), height  = 500, template='minty')
    

    return fig_city, fig_payment, fig_gender, fig_income_date,fig_product_income


# +++++++++ Run Server  =========== #
if __name__ == "__main__":
    app.run_server(port=8050, debug=False)