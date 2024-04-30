#! C:/Users/IT_TRAINEE/AppData/Local/Programs/Python/Python312/python.exe
# import sys
# print(sys.executable)  
print("Content-Type:text/HTML\n\r\n\r")

from flask import Flask
from dash import dash
# import dash_html_components as html
from dash import html 
from dash import dcc
import plotly.graph_objects as go
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np


pd_2 = pd.read_csv('https://raw.githubusercontent.com/Anmol3015/Plotly_Dash_examples/main/retail_sales.csv', sep=',')
pd_2['Date'] = pd.to_datetime(pd_2['Date'], format='%Y-%m-%d')

pd_2['Year'] = pd_2['Date'].dt.year


weekly_sales = pd_2.groupby(['Year', 'Date']).agg({'Weekly_Sales': 'sum'}).reset_index()

monthly_sales_df = pd_2.groupby(['month','Month']).agg({'Weekly_Sales':'sum'}).reset_index()


holiday_sales = pd_2[pd_2['IsHoliday'] == 1].groupby(['month'])['Weekly_Sales'].sum().reset_index().rename(columns={'Weekly_Sales':'Holiday_Sales'})


monthly_sales_df  = pd.merge(holiday_sales,monthly_sales_df,on = 'month', how = 'right').fillna(0)
 
monthly_sales_df['Weekly_Sales'] = monthly_sales_df['Weekly_Sales'].round(1)
monthly_sales_df['Holiday_Sales'] = monthly_sales_df['Holiday_Sales'].round(1)


weekly_sale = pd_2.groupby(['month','Month','Date']).agg({'Weekly_Sales':'sum'}).reset_index()
weekly_sale['week_no'] = weekly_sale.groupby(['Month'])['Date'].rank(method='min')


store_df=pd_2.groupby(['month','Month','Store']).agg({'Weekly_Sales':'sum'}).reset_index()
store_df['Store'] = store_df['Store'].apply(lambda x: 'Store'+" "+str(x))
store_df['Weekly_Sales'] = store_df['Weekly_Sales'].round(1)


dept_df=pd_2.groupby(['month','Month','Dept']).agg({'Weekly_Sales':'sum'}).reset_index()
dept_df['Dept'] = dept_df['Dept'].apply(lambda x: 'Dept'+" "+str(x))
dept_df['Weekly_Sales'] = dept_df['Weekly_Sales'].round(1)

fuel_df=pd_2.groupby(['month','Month','Fuel_Price']).agg({'Weekly_Sales':'sum'}).reset_index()
fuel_df['Fuel_Price'] = fuel_df['Fuel_Price'].apply(lambda x: 'Fuel_Price'+" "+str(x))
fuel_df['Weekly_Sales'] = fuel_df['Weekly_Sales'].round(1)

years = pd_2["Date"].dt.year.unique()
months = pd_2["Date"].dt.month_name().unique()
types = pd_2["Type"].unique()

server=Flask(__name__)
app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server
app.layout = html.Div([
    dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
#                         dbc.Col(html.Img(src=PLOTLY_LOGO, height="70px")),
                        dbc.Col(dbc.NavbarBrand("Retail Sales Dashboard", style={'color': 'white', 'fontSize': '40px',
                                                                                 'fontFamily': 'Times New Roman'})),
                    ],
                    align="center"
                ),
#                 href="https://plot.ly",
            ),
        ],
        color='#090059'
    ),
    dbc.Container([
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Select Month', style={'textAlign': 'center'}),
                        dcc.Dropdown(
                            id='dropdown_base',
                            options=[{'label': i, 'value': i} for i in monthly_sales_df.sort_values('month')['Month']],
                            value='Feb'
                        ),
                    ])
                ], style={'height': '130px',"box-shadow": "1px 2px 7px 0px grey"})
            ], width=3),
            dbc.Col([
                dbc.Card(id='card_num1', style={'height': '130px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
            dbc.Col([
                dbc.Card(id='card_num2', style={'height': '130px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
            dbc.Col([
                dbc.Card(id='card_num3', style={'height': '130px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
            dbc.Col([
                dbc.Card(id='card_num4', style={'height': '130px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
        ]),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(id='card_num5', style={'height': '350px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
            dbc.Col([
                dbc.Card(id='card_num6', style={'height': '350px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
            dbc.Col([
                dbc.Card(id='card_num7', style={'height': '350px',"box-shadow": "1px 2px 7px 0px grey"})
            ],width=3),
        ]),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(id='card_num8', style={'height': '350px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
            dbc.Col([
                dbc.Card(id='card_num9', style={'height': '350px',"box-shadow": "1px 2px 7px 0px grey"})
            ]),
        ]),
    ], style={'backgroundColor': '#f7f7f7'}, fluid=True)
])


@app.callback([
    Output('card_num1', 'children'),
    Output('card_num2', 'children'),
    Output('card_num3', 'children'),
    Output('card_num4', 'children'),
    Output('card_num5', 'children'),
    Output('card_num6', 'children'),
    Output('card_num7', 'children'),
    Output('card_num8', 'children'),
    Output('card_num9', 'children')
], [Input('dropdown_base', 'value')])
def update_cards(base):
    sales_base = monthly_sales_df.loc[monthly_sales_df['Month'] == base].reset_index()['Weekly_Sales'][0]
    holi_base = monthly_sales_df.loc[monthly_sales_df['Month'] == base].reset_index()['Holiday_Sales'][0]
    base_st_ct = pd_2.loc[pd_2['Month'] == base, 'Store'].drop_duplicates().count()
    base_dept_ct = pd_2.loc[pd_2['Month'] == base, 'Dept'].drop_duplicates().count()

    fig = go.Figure(data=[
        go.Scatter(x=weekly_sale.loc[weekly_sale['Month'] == base, 'week_no'],
                   y=weekly_sale.loc[weekly_sale['Month'] == base, 'Weekly_Sales'],
                   line=dict(color='firebrick', width=4),
                   name='{}'.format(base))
    ])

    fig.update_layout(plot_bgcolor='white',
                      margin=dict(l=40, r=5, t=60, b=40),
                      yaxis_tickprefix='$',
                      yaxis_ticksuffix='M')

    store_sales = store_df.loc[store_df['Month'] == base].sort_values('Weekly_Sales')
    store_names = store_sales['Store']
    store_sales_values = store_sales['Weekly_Sales']

    fig2 = go.Figure()

    
    fig2.add_trace(go.Bar(x=store_sales_values[:10], y=store_names[:10], orientation='h',
                          marker=dict(color='Indianred'),
                          text=store_sales_values[:10], textposition='outside',
                          name='Lowest Sales'))

    
    fig2.add_trace(go.Bar(x=store_sales_values[-10:], y=store_names[-10:], orientation='h',
                          marker=dict(color='#4863A0'),
                          text=store_sales_values[-10:], textposition='outside',
                          name='Highest Sales'))

    fig2.update_layout(plot_bgcolor='white',
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_tickprefix='$',
                       xaxis_ticksuffix='M',
#                        title='Stores with Highest and Lowest Sales ({})'.format(base),
                       title_x=0.5)
    
    type_counts = pd_2.loc[pd_2['Month'] == base, 'Type'].value_counts()
    fig3 = go.Figure(data=[go.Pie(labels=type_counts.index, values=type_counts.values)])

    fig3.update_layout(title='', plot_bgcolor='white')
    
    dept_sales = dept_df.loc[dept_df['Month'] == base].sort_values('Weekly_Sales', ascending=False).head(10)
    dept_names = dept_sales['Dept']
    dept_sales_values = dept_sales['Weekly_Sales']

    fig4 = go.Figure(data=[
        go.Bar(x=dept_names, y=dept_sales_values, marker_color='#4863A0')
    ])
    
    fig4.update_layout(plot_bgcolor='white',
                       margin=dict(l=40, r=5, t=60, b=40),
#                        xaxis_tickprefix='$',
#                        xaxis_ticksuffix='M',
#                        title='Top 7 Departments by Sales ({})'.format(base),
                       title_x=0.5)
    
    
    fuel_sales = fuel_df.loc[fuel_df['Month'] == base].sort_values('Fuel_Price')
    fuel_prices = fuel_sales['Fuel_Price']
    fuel_sales_values = fuel_sales['Weekly_Sales']
    
    fig5 = go.Figure(data=[
        go.Scatter(x=fuel_prices, y=fuel_sales_values, mode='lines+markers', marker_color='orange')
        
    ])
    
    fig5.update_layout(plot_bgcolor='white',
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_title='',
                       yaxis_title='',
#                        title='Weekly Sales vs. Fuel Price'
                      )
    
    
    return (
        dbc.CardBody([
            html.H6('Total sales', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
            html.H3('{0}{1}{2}'.format("$", sales_base, "M"), style={'color': '#090059', 'textAlign': 'center'})
        ]),
        dbc.CardBody([
            html.H6('Holiday Sales', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
            html.H3('{0}{1}{2}'.format("$", holi_base, "M"), style={'color': '#090059', 'textAlign': 'center'})
        ]),
        dbc.CardBody([
            html.H6('Total Stores', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
            html.H3('{}'.format(base_st_ct), style={'color': '#090059', 'textAlign': 'center'})
        ]),
        dbc.CardBody([
            html.H6('Total Departments', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
            html.H3('{}'.format(base_dept_ct), style={'color': '#090059', 'textAlign': 'center'})
        ]),
        dbc.CardBody([
            html.H6('Weekly Sales ', style={'fontWeight': 'bold', 'textAlign': 'center'}),
            dcc.Graph(figure=fig, style={'height': '250px'})
        ]),
        dbc.CardBody([
            html.H6('Top 7 Departments by sales', style={'fontWeight': 'bold', 'textAlign': 'center'}),
            dcc.Graph(figure=fig4, style={'height': '300px'})
        ]),
        
        dbc.CardBody([
            html.H6('Type Distribution', style={'fontWeight': 'bold', 'textAlign': 'center'}),
            dcc.Graph(figure=fig3, style={'height': '300px'})
        ]),
        dbc.CardBody([
            html.H6('Stores with Highest and Lowest Sales', style={'fontWeight': 'bold', 'textAlign': 'center'}),
            dcc.Graph(figure=fig2, style={'height': '300px'})
        ]),
        
        dbc.CardBody([
            html.H6('Fuel Prices on sales ', style={'fontWeight': 'bold', 'textAlign': 'center'}),
            dcc.Graph(figure=fig5, style={'height': '300px'})
        ])
        
    )


if __name__ == "__main__":
    app.run_server(debug=False)
