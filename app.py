# -*- coding: utf-8 -*-
"""
Created on Sun July 19 th 2020

@author: Azemar David
"""
import dash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_table 
from dash.exceptions import PreventUpdate
from dash_table import DataTable

import sqlite3
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol

import pandas as pd
import base64
import numpy as np
import math
import io
import json
from pandas.io.json import json_normalize
import time
from datetime import datetime

import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots


from waitress import serve

import dash_daq as daq


############################################################################################################################
############################################################################################################################
############################################################################################################################
#####################################     app   ############################################################################
############################################################################################################################	
############################################################################################################################
############################################################################################################################


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.config.suppress_callback_exceptions = True
server = app.server


############################################################################################################################
############################################################################################################################
############################################################################################################################
#####################################     data  ############################################################################
############################################################################################################################	
############################################################################################################################
############################################################################################################################


data_osamu = pd.read_csv("assets/Osamu_health_data.csv", delimiter=";",decimal=".",encoding = "ISO-8859-1",engine='python')


#picture
logo_1 = 'assets/add_logo.PNG'
logo_2 = 'assets/see_data_logo.PNG'
logo_3 = 'assets/doctor_report.PNG'
logo_4 = 'assets/temperature.PNG'

############################################################################################################################
############################################################################################################################
############################################################################################################################
#####################################     homepage   #########################################################################
############################################################################################################################	
############################################################################################################################
############################################################################################################################

#######  layout #########

layout_home = dbc.Container([
                    html.Br(),
                    dbc.Row([html.H2(children='Health Follow-Up Application',
                              style={
                                   'textAlign': 'center',
                                   'textJustify':'center',
                                   'height':'26px'
                                     })
                            ],justify="center"),
                    html.Br(),
                    dbc.Row([html.H4(children='Welcome Back Osamu Kimura !',
                              style={
                                   'textAlign': 'center',
                                   'textJustify':'center',
                                   'height':'26px'
                                     })
                            ],justify="center"),                    
                    html.Br(),                
                    html.Br(),
                    dbc.Row([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4("Add daily measures", className="card-title"),
                                    dbc.Row([
                                    dbc.CardImg(src='assets/add_logo.PNG',style={'height': '120px','width':'120px'}),                                
                                        ],justify='center'),
                                           ]),
                                dbc.CardFooter([           
                                         dbc.Button("Open", color="success",id="bt1"), 
                                               ],style={'align':'center'}),  
                                      ],style={'height': '250px','width':'300px','textAlign': 'center'}
                                    ),
                    ],justify="center"),
                    html.Br(),
                    dbc.Row([                          
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4("Explore the data", className="card-title"),
                                    dbc.Row([
                                    dbc.CardImg(src='assets/see_data_logo.PNG',style={'height': '120px','width':'120px'}),                                
                                        ],justify='center'),
                                           ]),
                                dbc.CardFooter([           
                                         dbc.Button("Open", color="success",id="bt2"), 
                                               ],style={'align':'center'}),  
                                      ],style={'height': '250px','width':'300px','textAlign': 'center'}
                                    ),
                    ],justify="center"),
                    html.Br(),                    
                    dbc.Row([          
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4("Send to doctor", className="card-title"),
                                    dbc.Row([
                                    dbc.CardImg(src='assets/doctor_report.PNG',style={'height': '120px','width':'120px'}),                                
                                        ],justify='center'),
                                    # html.P(
                                    #       "Detailled performance per location & category",
                                    #       className="card-text",
                                           ]),
                                dbc.CardFooter([           
                                         dbc.Button("Open", color="success",id="bt3"), 
                                               ],style={'align':'center'}),  
                                      ],style={'height': '250px','width':'300px','textAlign': 'center'}
                                    ),  
                    ],justify="center"),              
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Row([html.H6('©Datamink,V1.0 August 2020')],justify="center")
                            ],fluid=True)              


def App_home():
    layout =html.Div([layout_home
              ])
    return layout	

#######  callback #########

@app.callback(Output('url', 'pathname'),
              [Input('bt1', 'n_clicks'),
               Input('bt2', 'n_clicks'),
               Input('bt3', 'n_clicks')])
def display_page(n0,n1,n2):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "" 
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]   

        if button_id == 'bt1': 
            return "/adddata" 
        elif button_id == 'bt2':    
            return "/seedata"
        elif button_id == 'bt3':    
            return "/senddoctor"  
        else:
            return "" 


############################################################################################################################
############################################################################################################################
############################################################################################################################
#####################################     add data   #######################################################################
############################################################################################################################	
############################################################################################################################
############################################################################################################################



#######  layout #########

date_input = dbc.Form([
                 dbc.FormGroup([  
                   dbc.Row([dbc.Label("Select today's date")]),
                   html.Br(),
                   dbc.Row([dcc.DatePickerSingle(
                             id='selected_date',
                             max_date_allowed = datetime.today(),
                             month_format = 'MMM Do, YY',
                             with_portal = True,
                             placeholder ='Select Date')]),
                              ])
                     ])


weight_input = dbc.Card([
                    dbc.CardHeader([html.H4("Weight & activity")]),
                    dbc.CardBody([
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Weight"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="weight",
                                  placeholder="In KG",
                                  type="number",
                                  min=35,
                                  max=300,
                                  step=1),
                              ]),    
                      dbc.Col([
                        dbc.Label("Walking distance"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="walking_distance",
                                  placeholder="In Km",
                                  type="number",
                                  min=0,
                                  max=300,
                                  step=0.1),
                              ]),                                                                                                               
                     ],justify="center"),
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Running_distance"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="running_distance",
                                  placeholder="In Km",
                                  type="number",
                                  min=0,
                                  max=300,
                                  step=0.1),
                              ]),    
                      dbc.Col([
                        dbc.Label("Cycling distance"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="cycling_distance",
                                  placeholder="In Km",
                                  type="number",
                                  min=0,
                                  max=300,
                                  step=0.1),
                              ]),                                                                                                               
                     ],justify="center"),                     
                    ])
                    ],style={'width':'900px','textAlign': 'center'})


temperature_input = dbc.Card([
                    dbc.CardHeader([html.H4("Temperature")]),
                    dbc.CardBody([
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Morning - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='temperature_morning_time',
                                     value="Select range",
                                     options=[
                                         {"label":"4-5 am","value":"4-5 am"},
                                         {"label":"5-6 am","value":"5-6 am"},
                                         {"label":"6-7 am","value":"6-7 am"},
                                         {"label":"7-8 am","value":"7-8 am"},
                                         {"label":"8-9 am","value":"8-9 am"},
                                         {"label":"9-10 am","value":"9-10 am"},
                                         {"label":"10-11 am","value":"10-11 am"},
                                         {"label":"11-12 am","value":"11-12 am"},                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Temperature"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="morning_temperature",
                                  placeholder="Temperature in C°",
                                  type="number",
                                  min=35,
                                  max=42,
                                  step=0.1),
                              ]),                                                                                    
                     ],justify="center"),
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Afternoon - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='temperature_afternoon_time',
                                     value="Select range",
                                     options=[
                                         {"label":"12-13 pm","value":"12-13 pm"},
                                         {"label":"13-14 pm","value":"13-14 pm"},
                                         {"label":"14-15 pm","value":"14-15 pm"},
                                         {"label":"15-16 pm","value":"15-16 pm"},
                                         {"label":"16-17 pm","value":"16-17 pm"},
                                         {"label":"17-18 pm","value":"17-18 pm"},                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Temperature"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="afternoon_temperature",
                                  placeholder="Temperature in C°",
                                  type="number",
                                  min=35,
                                  max=42,
                                  step=0.1),
                              ]),                                                                                    
                     ],justify="center"),                     
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Evening - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='temperature_evening_time',
                                     value="Select range",
                                     options=[
                                         {"label":"18-19 pm","value":"18-19 pm"},
                                         {"label":"19-20 pm","value":"19-20 pm"},
                                         {"label":"20-21 pm","value":"20-21 pm"},
                                         {"label":"21-22 pm","value":"21-22 pm"},
                                         {"label":"22-23 pm","value":"22-23 pm"},
                                         {"label":"23-00 pm","value":"23-00 pm"}, 
                                         {"label":"00-04 am","value":"00-04 am"},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Temperature"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="evening_temperature",
                                  placeholder="Temperature in C°",
                                  type="number",
                                  min=35,
                                  max=42,
                                  step=0.1),
                              ]),                                                                                    
                     ],justify="center")  
                    ])
                    ],style={'width':'900px','textAlign': 'center'})


blood_sugar_input = dbc.Card([
                    dbc.CardHeader([html.H4("Blood sugar level")]),
                    dbc.CardBody([
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Morning - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='blood_morning_time',
                                     value="Select range",
                                     options=[
                                         {"label":"4-5 am","value":"4-5 am"},
                                         {"label":"5-6 am","value":"5-6 am"},
                                         {"label":"6-7 am","value":"6-7 am"},
                                         {"label":"7-8 am","value":"7-8 am"},
                                         {"label":"8-9 am","value":"8-9 am"},
                                         {"label":"9-10 am","value":"9-10 am"},
                                         {"label":"10-11 am","value":"10-11 am"},
                                         {"label":"11-12 am","value":"11-12 am"},                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Blood sugar"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="morning_blood",
                                  placeholder="In mg/dL",
                                  type="number",
                                  min=60,
                                  max=400,
                                  step=1),
                              ]),                                                                                    
                     ],justify="center"),
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Afternoon - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='blood_afternoon_time',
                                     value="Select range",
                                     options=[
                                         {"label":"12-13 pm","value":"12-13 pm"},
                                         {"label":"13-14 pm","value":"13-14 pm"},
                                         {"label":"14-15 pm","value":"14-15 pm"},
                                         {"label":"15-16 pm","value":"15-16 pm"},
                                         {"label":"16-17 pm","value":"16-17 pm"},
                                         {"label":"17-18 pm","value":"17-18 pm"},                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Blood sugar"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="afternoon_blood",
                                  placeholder="In mg/dL",
                                  type="number",
                                  min=60,
                                  max=400,
                                  step=1),
                              ]),                                                                                    
                     ],justify="center"),                     
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Evening - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='blood_evening_time',
                                     value="Select range",
                                     options=[
                                         {"label":"18-19 pm","value":"18-19 pm"},
                                         {"label":"19-20 pm","value":"19-20 pm"},
                                         {"label":"20-21 pm","value":"20-21 pm"},
                                         {"label":"21-22 pm","value":"21-22 pm"},
                                         {"label":"22-23 pm","value":"22-23 pm"},
                                         {"label":"23-00 pm","value":"23-00 pm"}, 
                                         {"label":"00-04 am","value":"00-04 am"},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Blood sugar"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="evening_blood",
                                  placeholder="In mg/dL",
                                  type="number",
                                  min=60,
                                  max=400,
                                  step=1),
                              ]),                                                                                    
                     ],justify="center")  
                    ])
                    ],style={'width':'900px','textAlign': 'center'})


blood_pressure_input = dbc.Card([
                    dbc.CardHeader([html.H4("Blood pressure")]),
                    dbc.CardBody([
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Morning - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='pressure_morning_time',
                                     value="Select range",
                                     options=[
                                         {"label":"4-5 am","value":"4-5 am"},
                                         {"label":"5-6 am","value":"5-6 am"},
                                         {"label":"6-7 am","value":"6-7 am"},
                                         {"label":"7-8 am","value":"7-8 am"},
                                         {"label":"8-9 am","value":"8-9 am"},
                                         {"label":"9-10 am","value":"9-10 am"},
                                         {"label":"10-11 am","value":"10-11 am"},
                                         {"label":"11-12 am","value":"11-12 am"},                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Diastolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="morning_diastolic",
                                  placeholder="In mmHg",
                                  type="number",
                                  min=40,
                                  max=250,
                                  step=5),
                              ]),                                                                                    
                      dbc.Col([
                        dbc.Label("Systolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="morning_systolic",
                                  placeholder="In mmHg",
                                  type="number",
                                  min=40,
                                  max=250,
                                  step=5),
                              ]),                                                                                    
                     ],justify="center"),
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Afternoon - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='pressure_afternoon_time',
                                     value="Select range",
                                     options=[
                                         {"label":"12-13 pm","value":"12-13 pm"},
                                         {"label":"13-14 pm","value":"13-14 pm"},
                                         {"label":"14-15 pm","value":"14-15 pm"},
                                         {"label":"15-16 pm","value":"15-16 pm"},
                                         {"label":"16-17 pm","value":"16-17 pm"},
                                         {"label":"17-18 pm","value":"17-18 pm"},                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Diastolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="afternoon_diastolic",
                                  placeholder="In mmHg",
                                  type="number",
                                  min=40,
                                  max=250,
                                  step=5),
                              ]),                                                                                    
                      dbc.Col([
                        dbc.Label("Systolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="afternoon_systolic",
                                  placeholder="In mmHg",
                                  type="number",
                                  min=40,
                                  max=250,
                                  step=5),
                              ]),                                                                                        
                     ],justify="center"),                     
                      dbc.Row([
                      dbc.Col([
                        dbc.Label("Evening - Time"),
                              ]),
                      dbc.Col([        
                        dcc.Dropdown(id='pressure_evening_time',
                                     value="Select range",
                                     options=[
                                         {"label":"18-19 pm","value":"18-19 pm"},
                                         {"label":"19-20 pm","value":"19-20 pm"},
                                         {"label":"20-21 pm","value":"20-21 pm"},
                                         {"label":"21-22 pm","value":"21-22 pm"},
                                         {"label":"22-23 pm","value":"22-23 pm"},
                                         {"label":"23-00 pm","value":"23-00 pm"}, 
                                         {"label":"00-04 am","value":"00-04 am"},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                                       ]
                               )
                              ]),  
                      dbc.Col([
                        dbc.Label("Diastolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="evening_diastolic",
                                  placeholder="In mmHg",
                                  type="number",
                                  min=40,
                                  max=250,
                                  step=5),
                              ]),                                                                                    
                      dbc.Col([
                        dbc.Label("Systolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="evening_systolic",
                                  placeholder="In mmHg",
                                  type="number",
                                  min=40,
                                  max=250,
                                  step=5),
                              ]),                                                                                      
                     ],justify="center")  
                    ])
                    ],style={'width':'900px','textAlign': 'center'})                    


consumption_input_1 = dbc.Card([
                    dbc.CardHeader([html.H4("Today's consumption")]),
                    dbc.CardBody([
                      dbc.Row([
                        dbc.Col([
                          daq.BooleanSwitch(id='smoking_switch',
                                          on=False,color="#9B51E0")
                                ]),
                        dbc.Col([
                           dbc.Label("Smoking"),
                                ]),    
                        dbc.Col([
                          daq.BooleanSwitch(id='alcool_switch',
                                          on=False,color="#9B51E0")
                                ]),
                        dbc.Col([
                           dbc.Label("Alcool"),
                                ]),                                                                                                      
                     ],justify="center"),
                      dbc.Row([
                        dbc.Col([
                          daq.BooleanSwitch(id='meat_switch',
                                          on=False,color="#9B51E0")
                                ]),
                        dbc.Col([
                           dbc.Label("Meat"),
                                ]),    
                        dbc.Col([
                          daq.BooleanSwitch(id='Junk_food_switch',
                                          on=False,color="#9B51E0")
                                ]),
                        dbc.Col([
                           dbc.Label("Junk food"),
                                ]),                                                                                                      
                     ],justify="center"),
                    ])
                    ],style={'width':'900px','textAlign': 'center'})                    



layout_add_measure=dbc.Container([
                    html.Br(),
                    dbc.Row([html.H2(children='Add daily measures',
                              style={
                                   'textAlign': 'center',
                                   'textJustify':'center',
                                   'height':'26px'
                                     })
                            ],justify="center"),
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                             date_input
                             ],justify="center",form=True,),
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                             weight_input
                             ],justify="center"),
                    html.Br(),
                    html.Br(),                                            
                    dbc.Row([
                             temperature_input
                             ],justify="center"),
                    html.Br(), 
                    html.Br(),                                                      
                    dbc.Row([
                             blood_sugar_input
                             ],justify="center"),
                    html.Br(),
                    html.Br(), 
                    dbc.Row([
                             blood_pressure_input
                             ],justify="center"),
                    html.Br(),
                    html.Br(), 
                    dbc.Row([
                             consumption_input_1
                             ],justify="center"),
                    html.Br(),
                    html.Br(),                  
                    dbc.Row([dbc.Button("Validate & save",id="button_validate_measure")],justify="center"),
                    html.Br(),
                    html.Br(),                                   
                    dbc.Row([html.H6('©Datamink,V1.0 August 2020')],justify="center")
                            ],fluid=True)  


def App_add_data():
    layout = layout_add_measure

    return layout

#######  callbacks #########


# @app.callback( 
#    [Output('weight', 'value'), 
#     Output('walking_distance', 'value'), 
#     Output('running_distance', 'value'), 
#     Output('cycling_distance', 'value'),
#     Output('temperature_morning_time', 'value'),
#     Output('morning_temperature', 'value'),
#     Output('temperature_afternoon_time', 'value'),
#     Output('afternoon_temperature', 'value'),
#     Output('temperature_evening_time', 'value'),
#     Output('evening_temperature', 'value'),
#     Output('blood_morning_time', 'value'),
#     Output('morning_blood', 'value'),
#     Output('blood_afternoon_time', 'value'),
#     Output('afternoon_blood', 'value'),
#     Output('blood_evening_time', 'value'),
#     Output('evening_blood', 'value'),
#     Output('pressure_morning_time', 'value'),
#     Output('morning_diastolic', 'value'),
#     Output('morning_systolic', 'value'),
#     Output('pressure_afternoon_time', 'value'),
#     Output('afternoon_diastolic', 'value'),
#     Output('afternoon_systolic', 'value'),
#     Output('pressure_evening_time', 'value'),
#     Output('evening_diastolic', 'value'),
#     Output('evening_systolic', 'value'),
#     Output('cycling_distance', 'value'),



    
    
    
    
#     ],         
#     [Input('launch_1', 'n_clicks')])
# def update_data_base_on_selected_date(n):







############################################################################################################################
############################################################################################################################
############################################################################################################################
############################################################################################################################
#####################################     callback APP  ####################################################################
############################################################################################################################	
############################################################################################################################
############################################################################################################################
############################################################################################################################


app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')])



@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname'),
            ])
def display_page(pathname):
    if pathname == '/adddata':
        return App_add_data() 
    elif pathname == '/home':
        return App_home()  
    else:
        return App_home() 




############################################################################################################################
############################################################################################################################
############################################################################################################################
############################################################################################################################
#####################################     app    ###########################################################################
############################################################################################################################	
############################################################################################################################
############################################################################################################################
############################################################################################################################



if __name__ == '__main__':
    #app.run_server(debug=False)#,host='10.200.13.38',port='5000')
    app.run_server(debug=True)#,host='10.200.13.38',port='8051')
    # app.run_server(debug=False)
    # serve(app, host='0.0.0.0', port=8000)
