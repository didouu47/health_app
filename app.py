# -*- coding: utf-8 -*-
"""
Created on Sun July 19 th 2020

@author: Azemar David
"""
import dash

import dash_core_components as dcc
import dash_html_components as html
from dash.dash import no_update
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
from datetime import date

import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots


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

data_osamu = pd.read_csv("assets/Osamu_health_data.csv", delimiter=";",decimal=".",parse_dates=['Date'],dayfirst=True)


# df = pd.read_csv("assets/Osamu_health_data.csv",delimiter=';',decimal='.',parse_dates=['Date'],dayfirst=True)


# # time.sleep(10)

# df = df[df['Date']>"01/01/2020"]
# df = df.replace(0,"")
# print(df)
# df['Month'] = pd.DatetimeIndex(df['Date']).month
# # df['Limit_up'] = 100
# # df['Limit_up_b'] = 80 
# # df['Limit_up_c'] = 120
# # df['Limit_up_2_b'] = 140
# # df['Limit_up_2_c'] = 180
# # df['Limit_down'] = 70
# print(df.columns)



# pivot = pd.pivot_table(df,
#                       index='Month',
#                       values = ['Sugar_morning','Sugar_evening','Weight','Temp_evening','Temp_morning'],                      
#                       # values = ['Sugar_morning','Sugar_evening','Limit_up','Limit_up_2_b','Limit_up_2_c',
#                       #           'Limit_down','Limit_up_b','Limit_up_c','Weight','Temp_evening','Temp_morning'],
#                       aggfunc = np.mean).reset_index()




# print(pivot)

# pivot['Month'] = pivot['Month'].replace({2:'February',
#                                      3:'March',
#                                      4:'April',
#                                      5:'May',
#                                      6:'June',
#                                      7:'July',
#                                      8:'August'
#                                   })

# pivot=pivot.round(2)

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
                    dbc.Row([html.H4(children='Health Follow-Up',
                              style={
                                   'textAlign': 'center',
                                   'textJustify':'center',
                                   'height':'26px'
                                     })
                            ],justify="center"),
                    html.Br(),
                    dbc.Row([html.H6(children='Welcome Back Osamu Kimura !',
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
               Input('bt3', 'n_clicks'),
               ])
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
#####################################     see data   #######################################################################
############################################################################################################################	
############################################################################################################################
############################################################################################################################


#######  static figures (to remove later) #########


# fig1 = go.Figure()
# fig1.add_trace(go.Scatter(x=df['Date'], y=df['Sugar_morning'],hovertext=df['Morning_sugar_time'],
#                     mode='lines',
#                     name='Sugar_morning'))
# fig1.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_b'],
#                      mode='lines',
#                      name='Normal range low'))
# fig1.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_c'],
#                      mode='lines',
#                      name='Normal range high'))
# fig1.update_layout(title="Daily Morning Blood Sugar vs normal range")
# fig1.update_layout(hovermode="x")


# fig2 = go.Figure(data=[
#     go.Bar(name='Average Morning Sugar', x=pivot['Month'], y=pivot['Sugar_morning']),
#     go.Scatter(name='Normal range low', x=pivot['Month'], y=pivot['Limit_up_b'],mode='lines'),
#     go.Scatter(name='Normal range high', x=pivot['Month'], y=pivot['Limit_up_c'],mode='lines')
# ])
# # Change the bar mode
# fig2.update_layout(barmode='group')
# fig2.update_layout(title="Monthly Average - Morning Blood Sugar")
# fig2.update_layout(hovermode="x")



# df['Month'] = df['Month'].replace({2:'February',
#                                      3:'March',
#                                      4:'April',
#                                      5:'May',
#                                      6:'June',
#                                      7:'July',
#                                      8:'August'
#                                   })

# fig3 = px.box(df, x='Month', y='Sugar_morning', points="all")
# fig3.update_layout(title="Monthly Statistical Analysis - Morning Blood Sugar")
# fig3.update_layout(hovermode="x")


# fig4 = go.Figure()
# fig4.add_trace(go.Scatter(x=df['Date'], y=df['Sugar_evening'],hovertext=df['Evening_sugar_time'],
#                     mode='lines',
#                     name='Sugar_evening'))
# fig4.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_2_b'],
#                      mode='lines',
#                      name='Normal range low'))
# fig4.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_2_c'],
#                      mode='lines',
#                      name='Normal range high'))
# fig4.update_layout(title="Daily Evening Blood Sugar vs normal range")
# fig4.update_layout(hovermode="x")


# fig5 = go.Figure(data=[
#     go.Bar(name='Average Evening Sugar', x=pivot['Month'], y=pivot['Sugar_evening']),
#     go.Scatter(name='Normal range low', x=pivot['Month'], y=pivot['Limit_up_2_b'],mode='lines'),
#     go.Scatter(name='Normal range high', x=pivot['Month'], y=pivot['Limit_up_2_c'],mode='lines')
# ])
# # Change the bar mode
# fig5.update_layout(barmode='group')
# fig5.update_layout(title="Monthly Average - Evening Blood Sugar")
# fig5.update_layout(hovermode="x")


# df['Month'] = df['Month'].replace({2:'February',
#                                      3:'March',
#                                      4:'April',
#                                      5:'May',
#                                      6:'June',
#                                      7:'July',
#                                      8:'August'
#                                   })

# fig6 = px.box(df, x='Month', y='Sugar_evening', points="all")
# fig6.update_layout(title="Monthly Statistical Analysis - Evening Blood Sugar")
# fig6.update_layout(hovermode="x")


# fig7 = go.Figure()
# fig7.add_trace(go.Scatter(x=pivot['Month'], y=pivot['Temp_evening'],
#                     mode='lines',
#                     name='Average Temperature evening'))
# fig7.add_trace(go.Scatter(x=pivot['Month'], y=pivot['Temp_morning'],
#                      mode='lines',
#                      name='Average Temperature morning'))
# fig7.update_layout(title="Monthly Average - Morning & Evening temperature")


# df['Month'] = df['Month'].replace({2:'February',
#                                      3:'March',
#                                      4:'April',
#                                      5:'May',
#                                      6:'June',
#                                      7:'July',
#                                      8:'August'
#                                   })

# fig8 = px.box(df, x='Month', y='Temp_morning', points="all")
# fig8.update_layout(title="Monthly Statistical Analysis - Temperature morning")
# fig8.update_layout(hovermode="x")


# df['Month'] = df['Month'].replace({2:'February',
#                                      3:'March',
#                                      4:'April',
#                                      5:'May',
#                                      6:'June',
#                                      7:'July',
#                                      8:'August'
#                                   })

# fig9 = px.box(df, x='Month', y='Temp_evening', points="all")
# fig9.update_layout(title="Monthly Statistical Analysis - Temperature evening")
# fig9.update_layout(hovermode="x")


# fig10 = go.Figure()
# fig10.add_trace(go.Scatter(x=df['Date'], y=df['Weight'],
#                     mode='lines',
#                     name='Weight'))

# fig10.update_layout(title="Daily Weight")
# fig10.update_layout(hovermode="x")


# fig11 = go.Figure()
# fig11.add_trace(go.Scatter(x=pivot['Month'], y=pivot['Weight'],
#                     mode='lines',
#                     name='Average Weight'))
# fig11.update_layout(title="Monthly Average - Weight")


# df['Month'] = df['Month'].replace({2:'February',
#                                      3:'March',
#                                      4:'April',
#                                      5:'May',
#                                      6:'June',
#                                      7:'July',
#                                      8:'August'
#                                   })

# fig12 = px.box(df, x='Month', y='Weight', points="all")
# fig12.update_layout(title="Monthly Statistical Analysis - Weight")
# fig12.update_layout(hovermode="x")



#######  figure #########

fig1 = dcc.Graph(id='daily_morning_sugar')#,style={'height': '450px','width':'550px'})
fig2 = dcc.Graph(id='monthly_morning_sugar')
fig3 = dcc.Graph(id='stats_morning_sugar')
fig4 = dcc.Graph(id='daily_evening_sugar')
fig5 = dcc.Graph(id='monthly_evening_sugar')
fig6 = dcc.Graph(id='stats_evening_sugar')
fig7 = dcc.Graph(id='monthly_average_temp')
fig8 = dcc.Graph(id='stats_morning_temp')
fig9 = dcc.Graph(id='stats_afternoon_temp')
fig10 = dcc.Graph(id='daily_weight')
fig11 = dcc.Graph(id='monthly_average_weight')
fig12 = dcc.Graph(id='stats_weight')


#######  layout #########



layout_see_data=dbc.Container([
                    html.Br(),
                    dbc.Row([html.H2(children='Data analysis',
                              style={
                                   'textAlign': 'center',
                                   'textJustify':'center',
                                   'height':'26px'
                                     })
                            ],justify="center"),
                    html.Br(),
                    # dbc.Row([
                    # dbc.Button("Home",id='home_see_data'),
                    #         ],justify="center"),                    
                    html.Br(),
                    dbc.Row([
                             fig1
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig2
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig3
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig4
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig5
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig6
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig7
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig8
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig9
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig10
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig11
                             ],justify="center",form=True,),
                    html.Br(),
                    dbc.Row([
                             fig12
                             ],justify="center",form=True,),
                    html.Br(),                                                                                                                                                                                                                                     
                    html.Br(),
                    html.Br(),
                    dbc.Row([html.H6('©Datamink,V1.0 August 2020')],justify="center")
                            ],fluid=True,id="explore_data")  








#######  callback #########


@app.callback( 
   [
    Output("daily_morning_sugar","figure"),
    Output("monthly_morning_sugar","figure"),
    Output("stats_morning_sugar","figure"),
    Output("daily_evening_sugar","figure"),
    Output("monthly_evening_sugar","figure"),
    Output("stats_evening_sugar","figure"),
    Output("monthly_average_temp","figure"),
    Output("stats_morning_temp","figure"),
    Output("stats_afternoon_temp","figure"),
    Output("daily_weight","figure"),
    Output("monthly_average_weight","figure"),
    Output("stats_weight","figure")
    ],
   [Input('url', 'pathname')],  
   )         
def update_chart_see_data(pathname):
  # ctx = dash.callback_context

  # if not ctx.triggered:
  #       return {},{},{},{},{},{},{},{},{},{},{},{} 
  # else:
  #       button_id = ctx.triggered[0]['prop_id'].split('.')[0]  

  # if button_id == 'update_see_data':
  if pathname == '/seedata':  
          
          df = pd.read_csv("assets/Osamu_health_data.csv",delimiter=';',decimal='.',parse_dates=['Date'],dayfirst=True)
          df = df[df['Date']>"01/01/2020"]
          df = df.replace(0,np.nan)
          print(df)
          df['Month'] = pd.DatetimeIndex(df['Date']).month
          df['Limit_up'] = 100
          df['Limit_up_b'] = 80 
          df['Limit_up_c'] = 120
          df['Limit_up_2_b'] = 140
          df['Limit_up_2_c'] = 180
          df['Limit_down'] = 70
          print(df.columns)
          print(df)
          pivot = pd.pivot_table(df,
                      index='Month',
                      # values = ['Sugar_morning','Sugar_evening','Weight','Temp_evening','Temp_morning'],                      
                      values = ['Sugar_morning','Sugar_evening','Limit_up','Limit_up_2_b','Limit_up_2_c',
                                'Limit_down','Limit_up_b','Limit_up_c','Weight','Temp_evening','Temp_morning'],
                      aggfunc = np.mean).reset_index()
          pivot['Month'] = pivot['Month'].replace({2:'February',
                                     3:'March',
                                     4:'April',
                                     5:'May',
                                     6:'June',
                                     7:'July',
                                     8:'August'
                                  })
          pivot=pivot.round(2)  
          print(pivot)
          fig1 = go.Figure()
          fig1.add_trace(go.Scatter(x=df['Date'], y=df['Sugar_morning'],hovertext=df['Morning_sugar_time'],
                    mode='lines',
                    name='Sugar_morning'))
          fig1.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_b'],
                     mode='lines',
                     name='Normal range low'))
          fig1.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_c'],
                     mode='lines',
                     name='Normal range high'))
          fig1.update_layout(title="Daily Morning Blood Sugar vs normal range")
          fig1.update_layout(hovermode="x")


          fig2 = go.Figure(data=[
              go.Bar(name='Average Morning Sugar', x=pivot['Month'], y=pivot['Sugar_morning']),
              go.Scatter(name='Normal range low', x=pivot['Month'], y=pivot['Limit_up_b'],mode='lines'),
              go.Scatter(name='Normal range high', x=pivot['Month'], y=pivot['Limit_up_c'],mode='lines')
          ])
          # Change the bar mode
          fig2.update_layout(barmode='group')
          fig2.update_layout(title="Monthly Average - Morning Blood Sugar")
          fig2.update_layout(hovermode="x")



          df['Month'] = df['Month'].replace({2:'February',
                                     3:'March',
                                     4:'April',
                                     5:'May',
                                     6:'June',
                                     7:'July',
                                     8:'August'
                                  })

          fig3 = px.box(df, x='Month', y='Sugar_morning', points="all")
          fig3.update_layout(title="Monthly Statistical Analysis - Morning Blood Sugar")
          fig3.update_layout(hovermode="x")


          fig4 = go.Figure()
          fig4.add_trace(go.Scatter(x=df['Date'], y=df['Sugar_evening'],hovertext=df['Evening_sugar_time'],
                    mode='lines',
                    name='Sugar_evening'))
          fig4.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_2_b'],
                     mode='lines',
                     name='Normal range low'))
          fig4.add_trace(go.Scatter(x=df['Date'], y=df['Limit_up_2_c'],
                     mode='lines',
                     name='Normal range high'))
          fig4.update_layout(title="Daily Evening Blood Sugar vs normal range")
          fig4.update_layout(hovermode="x")


          fig5 = go.Figure(data=[
              go.Bar(name='Average Evening Sugar', x=pivot['Month'], y=pivot['Sugar_evening']),
              go.Scatter(name='Normal range low', x=pivot['Month'], y=pivot['Limit_up_2_b'],mode='lines'),
              go.Scatter(name='Normal range high', x=pivot['Month'], y=pivot['Limit_up_2_c'],mode='lines')
          ])
          # Change the bar mode
          fig5.update_layout(barmode='group')
          fig5.update_layout(title="Monthly Average - Evening Blood Sugar")
          fig5.update_layout(hovermode="x")


          df['Month'] = df['Month'].replace({2:'February',
                                     3:'March',
                                     4:'April',
                                     5:'May',
                                     6:'June',
                                     7:'July',
                                     8:'August'
                                  })

          fig6 = px.box(df, x='Month', y='Sugar_evening', points="all")
          fig6.update_layout(title="Monthly Statistical Analysis - Evening Blood Sugar")
          fig6.update_layout(hovermode="x")


          fig7 = go.Figure()
          fig7.add_trace(go.Scatter(x=pivot['Month'], y=pivot['Temp_evening'],
                    mode='lines',
                    name='Average Temperature evening'))
          fig7.add_trace(go.Scatter(x=pivot['Month'], y=pivot['Temp_morning'],
                     mode='lines',
                     name='Average Temperature morning'))
          fig7.update_layout(title="Monthly Average - Morning & Evening temperature")


          df['Month'] = df['Month'].replace({2:'February',
                                     3:'March',
                                     4:'April',
                                     5:'May',
                                     6:'June',
                                     7:'July',
                                     8:'August'
                                  })

          fig8 = px.box(df, x='Month', y='Temp_morning', points="all")
          fig8.update_layout(title="Monthly Statistical Analysis - Temperature morning")
          fig8.update_layout(hovermode="x")


          df['Month'] = df['Month'].replace({2:'February',
                                     3:'March',
                                     4:'April',
                                     5:'May',
                                     6:'June',
                                     7:'July',
                                     8:'August'
                                  })

          fig9 = px.box(df, x='Month', y='Temp_evening', points="all")
          fig9.update_layout(title="Monthly Statistical Analysis - Temperature evening")
          fig9.update_layout(hovermode="x")


          fig10 = go.Figure()
          fig10.add_trace(go.Scatter(x=df['Date'], y=df['Weight'],
                    mode='lines',
                    name='Weight'))

          fig10.update_layout(title="Daily Weight")
          fig10.update_layout(hovermode="x")


          fig11 = go.Figure()
          fig11.add_trace(go.Scatter(x=pivot['Month'], y=pivot['Weight'],
                    mode='lines',
                    name='Average Weight'))
          fig11.update_layout(title="Monthly Average - Weight")


          df['Month'] = df['Month'].replace({2:'February',
                                     3:'March',
                                     4:'April',
                                     5:'May',
                                     6:'June',
                                     7:'July',
                                     8:'August'
                                  })

          fig12 = px.box(df, x='Month', y='Weight', points="all")
          fig12.update_layout(title="Monthly Statistical Analysis - Weight")
          fig12.update_layout(hovermode="x")  

          return fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11,fig12                      
 

  else:
    return {},{},{},{},{},{},{},{},{},{},{},{}  







def App_see_data():
    layout = layout_see_data

    return layout



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
                             month_format = 'DD/MM/YYYY',
                            # date = datetime.today(),
                             display_format = 'DD/MM/YYYY',
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
                                  style={'color':'black'},
                                  placeholder="In KG",
                                  type="number",
                                  value=0,
                                  min=0,
                                  max=300,
                                  step=0.1),
                              ]),    
                      dbc.Col([
                        dbc.Label("Walking distance"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="walking_distance",
                                  placeholder="In Km",
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  placeholder="In Km",
                                  type="number",
                                  min=0,
                                  value=0,
                                  max=300,
                                  step=0.1),
                              ]),    
                      dbc.Col([
                        dbc.Label("Cycling distance"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="cycling_distance",
                                  placeholder="In Km",
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
                                  max=250,
                                  step=5),
                              ]),                                                                                    
                      dbc.Col([
                        dbc.Label("Systolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="morning_systolic",
                                  placeholder="In mmHg",
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
                                  max=250,
                                  step=5),
                              ]),                                                                                    
                      dbc.Col([
                        dbc.Label("Systolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="afternoon_systolic",
                                  placeholder="In mmHg",
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
                                  max=250,
                                  step=5),
                              ]),                                                                                    
                      dbc.Col([
                        dbc.Label("Systolic"),
                              ]),    
                      dbc.Col([
                        dbc.Input(id="evening_systolic",
                                  placeholder="In mmHg",
                                  style={'color':'black'},
                                  type="number",
                                  min=0,
                                  value=0,
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
                    html.Div([
                         dash_table.DataTable(
                                                id="table_add_data",
                                                columns=[{"name": i, "id": i} for i in data_osamu.columns],
                                                data=data_osamu.to_dict('records'))
                            # ]),
                            ],style={'display': 'none'}),
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
                    dbc.Row([dbc.Button("Validate & save",id="button_validate_measure",color="success")],justify="center"),
                    html.Br(),
                    html.Br(),    
                    dbc.Modal([dbc.ModalBody("This is the content of the modal"),
                              #  dbc.ModalFooter(
                              #              dbc.Button("Close", id="close_modal_add_data", className="ml-auto")
                              #              )
                              ],id="modal_add_data"),                               
                    dbc.Row([html.H6('©Datamink,V1.0 August 2020')],justify="center")
                            ],fluid=True)  


def App_add_data():
    layout = layout_add_measure

    return layout

#######  callbacks #########


@app.callback( 
   [Output('weight', 'value'), 
    Output('walking_distance', 'value'), 
    Output('running_distance', 'value'), 
    Output('cycling_distance', 'value'),
    Output('temperature_morning_time', 'value'),
    Output('morning_temperature', 'value'),
    Output('temperature_afternoon_time', 'value'),
    Output('afternoon_temperature', 'value'),
    Output('temperature_evening_time', 'value'),
    Output('evening_temperature', 'value'),
    Output('blood_morning_time', 'value'),
    Output('morning_blood', 'value'),
    Output('blood_afternoon_time', 'value'),
    Output('afternoon_blood', 'value'),
    Output('blood_evening_time', 'value'),
    Output('evening_blood', 'value'),
    Output('pressure_morning_time', 'value'),
    Output('morning_diastolic', 'value'),
    Output('morning_systolic', 'value'),
    Output('pressure_afternoon_time', 'value'),
    Output('afternoon_diastolic', 'value'),
    Output('afternoon_systolic', 'value'),
    Output('pressure_evening_time', 'value'),
    Output('evening_diastolic', 'value'),
    Output('evening_systolic', 'value'),
    Output('smoking_switch', 'on'),
    Output('alcool_switch', 'on'),
    Output('meat_switch', 'on'),
    Output('Junk_food_switch','on')
    ],         
    [Input('selected_date', 'date')],
    [State('table_add_data','derived_virtual_data')])
def update_data_base_on_selected_date(date_value,data_table):
  

  data = pd.DataFrame(data_table)
  # print(data)
  # print(data.dtypes)
  data['Date'] = pd.to_datetime(data['Date'])

  if date_value is None:
    data = data
  else:
    data = data[data['Date']==date_value]


  data['Date'] = pd.to_datetime(data['Date'])
  data = data[data['Date']==date_value]

  # print(data)
  
  
  if len(data)>0:
    data = data[data['Date']==date_value]
    if data['Weight'].iloc[0]>0:
      weight = data['Weight'].iloc[0]
    else:
      weight =0  

    if data['Walking_distance'].iloc[0]>0:
      walking_distance = data['Walking_distance'].iloc[0]
    else:
      walking_distance=0

    if data['Running_distance'].iloc[0]>0:
      running_distance = data['Running_distance'].iloc[0]
    else:
      running_distance=0

    if data['Cycling_distance'].iloc[0]>0:
      cycling_distance = data['Cycling_distance'].iloc[0]
    else:
      cycling_distance=0

    if data['temperature_morning_time'].iloc[0] is None:
      temperature_morning_time = ""
    else:
      temperature_morning_time = data['temperature_morning_time'].iloc[0]
    
    if data['Temp_morning'].iloc[0]>0:
      morning_temperature = data['Temp_morning'].iloc[0]
    else:
      morning_temperature = 0

    if data['temperature_afternoon_time'].iloc[0] is None:
      temperature_afternoon_time = ""
    else:
      temperature_afternoon_time = data['temperature_afternoon_time'].iloc[0]

    if data['Temp_afternoon'].iloc[0]>0:
      afternoon_temperature = data['Temp_afternoon'].iloc[0]
    else:
      afternoon_temperature =0
    
    if data['temperature_evening_time'].iloc[0] is None:
      temperature_evening_time = ""
    else:
      temperature_evening_time = data['temperature_evening_time'].iloc[0]
    
    if data['Temp_evening'].iloc[0]>0:
      evening_temperature = data['Temp_evening'].iloc[0]
    else:
      evening_temperature = 0

    if data['Morning_sugar_time'].iloc[0] is None:
      blood_morning_time =""
    else:
      blood_morning_time = data['Morning_sugar_time'].iloc[0]

    if data['Sugar_morning'].iloc[0]>0:
      morning_blood = data['Sugar_morning'].iloc[0]
    else:
      morning_blood = 0

    if data['Afternoon_sugar_time'].iloc[0] is None:
      blood_afternoon_time = ""
    else:
      blood_afternoon_time = data['Afternoon_sugar_time'].iloc[0]

    if data['Sugar_afternoon'].iloc[0]>0:
      afternoon_blood = data['Sugar_afternoon'].iloc[0]
    else:
      afternoon_blood = 0

    if data['Evening_sugar_time'].iloc[0] is None:
      blood_evening_time=""
    else:
      blood_evening_time = data['Evening_sugar_time'].iloc[0]
    
    if data['Sugar_evening'].iloc[0]>0:
      evening_blood = data['Sugar_evening'].iloc[0]
    else:
      evening_blood = 0

    if data['Morning_blood_pressure_time'].iloc[0] is None:
      pressure_morning_time=""
    else:
      pressure_morning_time = data['Morning_blood_pressure_time'].iloc[0]

    if data['morning_bp_diastolique'].iloc[0]>0:
      morning_diastolic = data['morning_bp_diastolique'].iloc[0]
    else:
      morning_diastolic = 0

    if data['morning_bp_systolique'].iloc[0]>0:
      morning_systolic = data['morning_bp_systolique'].iloc[0]
    else:
      morning_systolic = 0
    
    if data['Afternoon_blood_pressure_time'].iloc[0] is None:
      pressure_afternoon_time = ""
    else:
      pressure_afternoon_time = data['Afternoon_blood_pressure_time'].iloc[0]
    
    if data['afternoon_bp_diastolique'].iloc[0]>0:
      afternoon_diastolic = data['afternoon_bp_diastolique'].iloc[0]
    else:
      afternoon_diastolic = 0
  
    if data['afternoon_bp_systolique'].iloc[0]>0:
      afternoon_systolic = data['afternoon_bp_systolique'].iloc[0]
    else:
      afternoon_systolic = 0

    if data['Evening_blood_pressure_time'].iloc[0] is None:
      pressure_evening_time = ""
    else:
      pressure_evening_time = data['Evening_blood_pressure_time'].iloc[0]
    
    if data['evening_bp_diastolique'].iloc[0]>0:
      evening_diastolic = data['evening_bp_diastolique'].iloc[0]
    else:
      evening_diastolic = 0

    if data['evening_bp_systolique'].iloc[0]>0:
      evening_systolic = data['evening_bp_systolique'].iloc[0]
    else:
      evening_systolic = 0  

    if data['smoking'].iloc[0] == True:
      smoking_switch = True
    else:
      smoking_switch = False        

    if data['alcool'].iloc[0] ==True:
      alcool_switch = True
    else:
      alcool_switch = False 

    if data['meat'].iloc[0] ==True:
      meat_switch = True
    else:
      meat_switch = False 

    if data['junk_food'].iloc[0] ==True:
      Junk_food_switch = True
    else:
      Junk_food_switch = False 

    return  weight, walking_distance,running_distance,cycling_distance,temperature_morning_time,morning_temperature,temperature_afternoon_time,afternoon_temperature,temperature_evening_time,evening_temperature,blood_morning_time,morning_blood,blood_afternoon_time,afternoon_blood,blood_evening_time,evening_blood,pressure_morning_time,morning_diastolic,morning_systolic,pressure_afternoon_time,afternoon_diastolic,afternoon_systolic,pressure_evening_time,evening_diastolic,evening_systolic,smoking_switch,alcool_switch,meat_switch,Junk_food_switch
  
  elif len(data)>1:
    return "","","","","","","","","","","","","","","","","","","","","","","","","",False,False,False,False
  else:
    return 0,0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,"",0,0,"",0,0,False,False,False,False



# @app.callback( 
#     [
#     Output('weight', 'style'), 
#     Output('walking_distance', 'style'), 
#     Output('running_distance', 'style'), 
#     Output('cycling_distance', 'style'),
#     Output('temperature_morning_time', 'style'),
#     Output('morning_temperature', 'style'),
#     Output('temperature_afternoon_time', 'style'),
#     Output('afternoon_temperature', 'style'),
#     Output('temperature_evening_time', 'style'),
#     Output('evening_temperature', 'style'),
#     Output('blood_morning_time', 'style'),
#     Output('morning_blood', 'style'),
#     Output('blood_afternoon_time', 'style'),
#     Output('afternoon_blood', 'style'),
#     Output('blood_evening_time', 'style'),
#     Output('evening_blood', 'style'),
#     Output('pressure_morning_time', 'style'),
#     Output('morning_diastolic', 'style'),
#     Output('morning_systolic', 'style'),
#     Output('pressure_afternoon_time', 'style'),
#     Output('afternoon_diastolic', 'style'),
#     Output('afternoon_systolic', 'style'),
#     Output('pressure_evening_time', 'style'),
#     Output('evening_diastolic', 'style'),
#     Output('evening_systolic', 'style')],
#    [Input('weight', 'value'), 
#     Input('walking_distance', 'value'), 
#     Input('running_distance', 'value'), 
#     Input('cycling_distance', 'value'),
#     Input('temperature_morning_time', 'value'),
#     Input('morning_temperature', 'value'),
#     Input('temperature_afternoon_time', 'value'),
#     Input('afternoon_temperature', 'value'),
#     Input('temperature_evening_time', 'value'),
#     Input('evening_temperature', 'value'),
#     Input('blood_morning_time', 'value'),
#     Input('morning_blood', 'value'),
#     Input('blood_afternoon_time', 'value'),
#     Input('afternoon_blood', 'value'),
#     Input('blood_evening_time', 'value'),
#     Input('evening_blood', 'value'),
#     Input('pressure_morning_time', 'value'),
#     Input('morning_diastolic', 'value'),
#     Input('morning_systolic', 'value'),
#     Input('pressure_afternoon_time', 'value'),
#     Input('afternoon_diastolic', 'value'),
#     Input('afternoon_systolic', 'value'),
#     Input('pressure_evening_time', 'value'),
#     Input('evening_diastolic', 'value'),
#     Input('evening_systolic', 'value')
#     ])         
# def update_color_input_selected_date(weight,walking_distance,running_distance,cycling_distance,temperature_morning_time,morning_temperature,temperature_afternoon_time,afternoon_temperature,temperature_evening_time,evening_temperature,blood_morning_time,morning_blood,blood_afternoon_time,afternoon_blood,blood_evening_time,evening_blood,pressure_morning_time,morning_diastolic,morning_systolic,pressure_afternoon_time,afternoon_diastolic,afternoon_systolic,pressure_evening_time,evening_diastolic,evening_systolic):

#   if weight:
#     weight_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     weight_style ={}

#   if walking_distance is None:
#     walking_distance_style = {'background': 'white','color':'black'}
#   else:
#     walking_distance_style ={'background': 'rgb(65,171,93)','color':'white'}

#   if running_distance is None:
#     running_distance_style = {'background': 'white','color':'black'}
#   else:
#     running_distance_style = {'background': 'rgb(65,171,93)','color':'white'}

#   if cycling_distance is None:
#     cycling_distance_style = {'background': 'white','color':'black'}
#   else:
#     cycling_distance_style = {'background': 'rgb(65,171,93)','color':'white'}

#   if temperature_morning_time is None:
#     temperature_morning_time_style = {'background': 'white','color':'black'}
#   else:
#     temperature_morning_time_style = {'background': 'rgb(65,171,93)','color':'white'}

#   if morning_temperature !="":
#     morning_temperature_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     morning_temperature_style ={}

#   if temperature_afternoon_time !="":
#     temperature_afternoon_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     temperature_afternoon_time_style ={}

#   if afternoon_temperature !="":
#     afternoon_temperature_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     afternoon_temperature_style ={}

#   if temperature_evening_time !="":
#     temperature_evening_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     temperature_evening_time_style ={}

#   if evening_temperature !="":
#     evening_temperature_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     evening_temperature_style ={}

#   if blood_morning_time !="":
#     blood_morning_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     blood_morning_time_style ={}

#   if morning_blood !="":
#     morning_blood_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     morning_blood_style ={}

#   if blood_afternoon_time !="":
#     blood_afternoon_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     blood_afternoon_time_style ={}

#   if afternoon_blood !="":
#     afternoon_blood_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     afternoon_blood_style ={}

#   if blood_evening_time !="":
#     blood_evening_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     blood_evening_time_style ={}

#   if evening_blood !="":
#     evening_blood_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     evening_blood_style ={}

#   if pressure_morning_time !="":
#     pressure_morning_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     pressure_morning_time_style ={}

#   if morning_diastolic !="":
#     morning_diastolic_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     morning_diastolic_style ={}

#   if morning_systolic !="":
#     morning_systolic_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     morning_systolic_style ={}

#   if pressure_afternoon_time !="":
#     pressure_afternoon_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     pressure_afternoon_time_style ={}

#   if afternoon_diastolic !="":
#     afternoon_diastolic_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     afternoon_diastolic_style ={}

#   if afternoon_systolic !="":
#     afternoon_systolic_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     afternoon_systolic_style ={}

#   if pressure_evening_time !="":
#     pressure_evening_time_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     pressure_evening_time_style ={}

#   if evening_diastolic !="":
#     evening_diastolic_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     evening_diastolic_style ={}

#   if evening_systolic !="":
#     evening_systolic_style = {'background': 'rgb(65,171,93)','color':'white'}
#   else:
#     evening_systolic_style ={}                                                                                        




#   return weight_style,walking_distance_style,running_distance_style,cycling_distance_style,temperature_morning_time_style,morning_temperature_style,temperature_afternoon_time_style,afternoon_temperature_style,temperature_evening_time_style,evening_temperature_style,blood_morning_time_style,morning_blood_style,blood_afternoon_time_style,afternoon_blood_style,blood_evening_time_style,evening_blood_style,pressure_morning_time_style,morning_diastolic_style,morning_systolic_style,pressure_afternoon_time_style,afternoon_diastolic_style,afternoon_systolic_style,pressure_evening_time_style,evening_diastolic_style,evening_systolic_style
 

@app.callback( 
   [Output("modal_add_data","is_open"),
    Output("table_add_data","data")],
    # Output("table_add_data","columns")],
   [Input('button_validate_measure', 'n_clicks')], 
   [State("modal_add_data","is_open"),
    State('selected_date', 'date'),       
    State('weight', 'value'), 
    State('walking_distance', 'value'), 
    State('running_distance', 'value'), 
    State('cycling_distance', 'value'),
    State('temperature_morning_time', 'value'),
    State('morning_temperature', 'value'),
    State('temperature_afternoon_time', 'value'),
    State('afternoon_temperature', 'value'),
    State('temperature_evening_time', 'value'),
    State('evening_temperature', 'value'),
    State('blood_morning_time', 'value'),
    State('morning_blood', 'value'),
    State('blood_afternoon_time', 'value'),
    State('afternoon_blood', 'value'),
    State('blood_evening_time', 'value'),
    State('evening_blood', 'value'),
    State('pressure_morning_time', 'value'),
    State('morning_diastolic', 'value'),
    State('morning_systolic', 'value'),
    State('pressure_afternoon_time', 'value'),
    State('afternoon_diastolic', 'value'),
    State('afternoon_systolic', 'value'),
    State('pressure_evening_time', 'value'),
    State('evening_diastolic', 'value'),
    State('evening_systolic', 'value'),
    State('smoking_switch', 'on'),
    State('alcool_switch', 'on'),
    State('meat_switch', 'on'),
    State('Junk_food_switch', 'on'),
    State("table_add_data","derived_virtual_data")]  
   )         
def update_table_data_and_source(n1,is_open,selected_date,weight,walking_distance,running_distance,cycling_distance,temperature_morning_time,morning_temperature,temperature_afternoon_time,afternoon_temperature,temperature_evening_time,evening_temperature,blood_morning_time,morning_blood,blood_afternoon_time,afternoon_blood,blood_evening_time,evening_blood,pressure_morning_time,morning_diastolic,morning_systolic,pressure_afternoon_time,afternoon_diastolic,afternoon_systolic,pressure_evening_time,evening_diastolic,evening_systolic,smoking_switch,alcool_switch,meat_switch,Junk_food_switch,data_table):

    fi1 = pd.DataFrame(columns=['Date', 'Morning_sugar_time', 'Sugar_morning',
       'temperature_morning_time', 'Temp_morning', 'Afternoon_sugar_time',
       'Sugar_afternoon', 'temperature_afternoon_time', 'Temp_afternoon',
       'Evening_sugar_time', 'Sugar_evening', 'temperature_evening_time',
       'Temp_evening', 'Weight', 'morning_bp_diastolique',
       'morning_bp_systolique', 'afternoon_bp_diastolique',
       'afternoon_bp_systolique', 'evening_bp_diastolique',
       'evening_bp_systolique', 'Morning_blood_pressure_time',
       'Afternoon_blood_pressure_time', 'Evening_blood_pressure_time',
       'Walking_distance', 'Running_distance', 'Cycling_distance', 'smoking',
       'alcool', 'coffee', 'dessert', 'junk_food','meat'])

      # fi1['Date']=11 
      # print(fi1['Date'])

    fi1['Date'] = [selected_date]
    fi1['Weight'] = [float(weight)]
    fi1['Walking_distance'] = [float(walking_distance)]
    fi1['Running_distance'] = [float(running_distance)]
    fi1['Cycling_distance'] = [float(cycling_distance)]
    fi1['temperature_morning_time'] = [temperature_morning_time]
    fi1['Temp_morning'] = [float(morning_temperature)]
    fi1['temperature_afternoon_time'] = [temperature_afternoon_time]
    fi1['Temp_afternoon'] = [float(afternoon_temperature)]
    fi1['temperature_evening_time'] = [temperature_evening_time]
    fi1['Temp_evening'] = [float(evening_temperature)]
    fi1['Morning_sugar_time'] = [blood_morning_time]
    fi1['Sugar_morning'] = [int(morning_blood)]
    fi1['Afternoon_sugar_time'] = [blood_afternoon_time]
    fi1['Sugar_afternoon'] = [int(afternoon_blood)]
    fi1['Evening_sugar_time'] = [blood_evening_time]
    fi1['Sugar_evening'] = [int(evening_blood)]
    fi1['Morning_blood_pressure_time'] = [pressure_morning_time]
    fi1['morning_bp_diastolique'] = [int(morning_diastolic)]
    fi1['morning_bp_systolique'] = [int(morning_systolic)]
    fi1['Afternoon_blood_pressure_time'] = [pressure_afternoon_time]
    fi1['afternoon_bp_diastolique'] = [int(afternoon_diastolic)]
    fi1['afternoon_bp_systolique'] = [int(afternoon_systolic)]
    fi1['Evening_blood_pressure_time'] = [pressure_evening_time]
    fi1['evening_bp_diastolique'] = [int(evening_diastolic)]
    fi1['evening_bp_systolique'] = [int(evening_systolic)]
    fi1['smoking'] = [smoking_switch]
    fi1['alcool'] = [alcool_switch]
    fi1['meat'] = [meat_switch]
    fi1['junk_food'] = [Junk_food_switch]

    # to update later
    fi1['coffee'] = ["FALSE"]
    fi1['dessert'] = ["FALSE"]
      
    # data = pd.DataFrame(data_table)
    # data['Date'] = pd.to_datetime(data['Date'])
    # data = data[data['Date']==selected_date]

    # # data = data_osamu[data_osamu['Date']!=selected_date]
    # data = data.append(fi1,ignore_index=True)
    # data['Date'] = pd.to_datetime(data['Date'])
    # data = data.sort_values(by='Date',ascending=True)
    
    # columns_fig=[
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},
    #          {'name':'Sales Gr%','id':'Sales Gr%','type': 'numeric'},]



    ctx = dash.callback_context

    if not ctx.triggered:
      data_fig = data_osamu.to_dict('records')
      return is_open,no_update

    else:
      button_id = ctx.triggered[0]['prop_id'].split('.')[0]   

      if button_id == 'button_validate_measure': 

        data = pd.DataFrame(data_table)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data[data['Date']!=selected_date]
        data = data.append(fi1,ignore_index=True)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.sort_values(by='Date',ascending=True)        
        data_fig=data.to_dict('records')
        # print(data)
        data.to_csv ("assets/Osamu_health_data.csv",sep = ';',encoding = "utf-8", index = None)

        return not is_open,data_fig 

      else:
        data_fig = data_osamu.to_dict('records')
        
        return is_open,no_update 








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
    elif pathname == '/seedata':
        return App_see_data()
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
