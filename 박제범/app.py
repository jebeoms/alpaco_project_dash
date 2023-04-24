#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import dash
import jupyter_dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import datetime as dt





# In[2]:


df = pd.read_csv('subscription_log.csv')

df.dropna(subset=['price'], inplace=True)
df.dropna(subset=['target_customer'], inplace=True)
df['created_at'] = pd.to_datetime(df['created_at'])
df['created_Ym'] = df['created_at'].dt.strftime('%Y-%m')
print(df.shape)


# In[3]:


df = df.replace({'bigBiz':'큰 사업체', 'middleBiz':'중간 사업체', 'smallBiz':'작은 사업체', 'personal':'개인'})
df.head()


# In[4]:


df_non_refund = df[df['refund_id'].isnull()==True]


# In[5]:


df_refund = df[df['refund_id'].isnull()!=True]


# In[6]:


customer_count = df_non_refund.groupby('target_customer')['price'].count().reset_index()


# In[7]:


customer_price_sum = df_non_refund.groupby('target_customer')['price'].sum().reset_index()


# In[8]:


refund_count = df_refund.groupby('target_customer')['price'].count().reset_index()


# In[9]:


customer_count.columns = ['고객 유형', '매출 건수']

customer_count


# In[10]:


customer_price_sum.columns = ['고객 유형', '매출']

customer_price_sum


# In[11]:


refund_rate_data = {
    '고객 유형':['개인', '작은 사업체', '중간 사업체', '큰 사업체'],
    '환불율':[625*100/(625+27065), 70*100/(70+2881), 51*100/(51+157), 0]
}
refund_rate = pd.DataFrame(refund_rate_data)
refund_rate


# In[12]:


price_per_gun_data = {
    '고객 유형':['개인', '작은 사업체', '중간 사업체', '큰 사업체'],
    '건당 매출':[208552405.0/27065, 161282030.0/2881, 27938600.0/157, 3935340.0/6]
}
price_per_gun = pd.DataFrame(price_per_gun_data)
price_per_gun


# In[13]:


fig1 = px.pie(customer_count, values='매출 건수', names='고객 유형',color_discrete_sequence=['rgb(78,94,160)', 'rgb(92,162,143)','rgb(232,201,92)', 'rgb(203,67,66)'])
fig1.update_layout(
    title={
        'text':'매출 건수',
        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    showlegend = False,
    margin=dict(t=35, b=5, l=0, r=0),
    
)
fig1.update_traces(textposition='inside', textinfo='percent+label')


# In[14]:


fig2 = px.pie(customer_price_sum, values='매출', names='고객 유형',color_discrete_sequence=['rgb(78,94,160)', 'rgb(92,162,143)','rgb(232,201,92)', 'rgb(203,67,66)'])
fig2.update_layout(
    title={
        'text':'매출',
        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    showlegend = False,
    margin=dict(t=35, b=5, l=0, r=0)
)
fig2.update_traces(textposition='inside', textinfo='percent+label')


# In[15]:


fig3 = px.bar(refund_rate, x='고객 유형', y='환불율',title="고객 유형별 환불율", text_auto = True, 
              color_discrete_sequence=['rgb(78,94,160)'])
fig3.update_layout(
    title={

        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    showlegend = False,
    margin=dict(t=35, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None, yaxis_visible=False,
    plot_bgcolor='rgba(0,0,0,0)'
)
fig3.update_traces(texttemplate='%{y:.1f}')


# In[16]:


fig4 = px.bar(price_per_gun, x='고객 유형', y='건당 매출',title="고객 유형별 건당 매출", text_auto = True,
             color_discrete_sequence=['rgb(92,162,143)'])
fig4.update_layout(
    title={

        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    showlegend = False,
    margin=dict(t=35, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None, yaxis_visible=False,
    plot_bgcolor='rgba(0,0,0,0)'
)
fig4.update_traces(texttemplate='%{y:.2s}')


# In[17]:


df_refund_middle = df_refund[df_refund['target_customer']=='중간 사업체']
df_non_refund_middle = df_non_refund[df_non_refund['target_customer']=='중간 사업체']


# In[18]:


refund_Ym = df_refund_middle.groupby('created_Ym')['price'].count().reset_index()
refund_Ym.columns = ['created_Ym', '환불 건수']
refund_Ym


# In[19]:


non_refund_Ym = df_non_refund_middle.groupby('created_Ym')['price'].count().reset_index()
non_refund_Ym.columns = ['created_Ym', '환불 하지 않은 건수']
non_refund_Ym


# In[20]:


middle_Ym = pd.merge(left = refund_Ym, right = non_refund_Ym, on='created_Ym', how='outer')
middle_Ym = middle_Ym.sort_values('created_Ym', ascending=True)
middle_Ym


# In[21]:


fig5 = px.bar(middle_Ym, x="created_Ym", y=["환불 건수", "환불 하지 않은 건수"], title="환불 건수와 환불 하지 않은 건수",
             color_discrete_sequence=['rgb(203,67,66)','rgb(78,94,160)'])
fig5.update_layout(
    title={
        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    margin=dict(t=65, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None,
    legend=dict(
    title='',
    orientation='h',
    yanchor="top",
    y=1.12,
    xanchor="left",
    x=0.01
    ),
    plot_bgcolor='rgba(0,0,0,0)'
)


# In[22]:


df_non_refund_personal = df_non_refund[df_non_refund['target_customer']=='개인']
personal = df_non_refund_personal.groupby('created_Ym')['price'].sum().reset_index()

df_non_refund_small = df_non_refund[df_non_refund['target_customer']=='작은 사업체']
small = df_non_refund_small.groupby('created_Ym')['price'].sum().reset_index()

df_non_refund_middle = df_non_refund[df_non_refund['target_customer']=='중간 사업체']
middle = df_non_refund_middle.groupby('created_Ym')['price'].sum().reset_index()

df_non_refund_big = df_non_refund[df_non_refund['target_customer']=='큰 사업체']
big = df_non_refund_big.groupby('created_Ym')['price'].sum().reset_index()


# In[23]:


fig6 = px.line(personal, x='created_Ym', y='price',markers = True)
fig6.update_layout(
    title={
        'text':'개인에게서 얻은 매출',
        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    margin=dict(t=35, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None,
    plot_bgcolor='rgba(0,0,0,0)'
)

fig6.update_traces(line_color='rgb(213,98,130)', line_width=5,  line=dict(dash='dashdot'), 
                  marker=dict(size=10, symbol='circle'))

fig7 = px.line(small, x='created_Ym', y='price',markers = True)
fig7.update_layout(
    title={
        'text':'작은 사업체에게서 얻은 매출',
        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    margin=dict(t=35, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None,
    plot_bgcolor='rgba(0,0,0,0)'
)

fig7.update_traces(line_color='rgb(213,98,130)', line_width=5,  line=dict(dash='dashdot'), 
                  marker=dict(size=10, symbol='circle'))

fig8 = px.line(middle, x='created_Ym', y='price',markers = True)
fig8.update_layout(
    title={
        'text':'중간 사업체에게서 얻은 매출',
        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    margin=dict(t=35, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None,
    plot_bgcolor='rgba(0,0,0,0)'
)

fig8.update_traces(line_color='rgb(213,98,130)', line_width=5,  line=dict(dash='dashdot'), 
                  marker=dict(size=10, symbol='circle'))

fig9 = px.line(big, x='created_Ym', y='price',markers = True)
fig9.update_layout(
    title={
        'text':'큰 사업체에게서 얻은 매출',
        'font': {'family': "verdana", 'size': 20},
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center'
    },
    margin=dict(t=35, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None,
    plot_bgcolor='rgba(0,0,0,0)'
)
fig9.update_traces(line_color='rgb(213,98,130)', line_width=5,  line=dict(dash='dashdot'), 
                  marker=dict(size=10, symbol='circle'))


# In[24]:


# data = {
#     'iso_alpha': ['USA', 'BRA', 'ESP', 'GBR', 'FRA', 'DEU', 'KOR', 'AUS', 'JPN'],
#     'pop': [8600, 10600, 1700, 1660, 1650, 1900, 1750, 600, 1850],
#     'country': ['미국', '브라질', '스페인', '영국', '프랑스', '독일', '한국', '호주', '일본']
# }

# df = pd.DataFrame(data)

# fig5 = px.scatter_geo(df, locations="iso_alpha", 
#                      hover_name="country", size="pop",
#                      projection="natural earth",
#                      size_max = 40)

# fig5.update_layout(
#     title={
#         'text':'늘어난 크리에이터 규모',
#         'font': {'family': "verdana", 'size': 20},
#         'x': 0.5,
#         'xanchor': 'center'
#     }
# )


# In[25]:


sfx = pd.read_csv('sfx.csv')
song = pd.read_csv('song.csv') 


# In[26]:


song.drop(['bpm', 'length'], axis=1, inplace=True)
sfx.drop('playtime', axis=1, inplace=True)

song['music_type'] = 'song'
sfx['music_type'] = 'sfx'

song_sfx = pd.concat([song, sfx], axis=0)

song_sfx['created_at'] = pd.to_datetime(song_sfx['created_at'])
song_sfx['created_at'] = song_sfx['created_at'].dt.strftime('%Y-%m')


# In[27]:


song_sfx.loc[song_sfx['grade'].isin(['1.0.S', '3.0.S']), 'grade'] = 'S'
song_sfx.loc[song_sfx['grade'].isin(['1.1.A', '3.1.A', '2.1.A']), 'grade'] = 'A'
song_sfx.loc[song_sfx['grade'].isin(['1.2.B', '3.2.B']), 'grade'] = 'B'
song_sfx.loc[song_sfx['grade'].isin(['1.3.C', '3.3.C']), 'grade'] = 'C'
song_sfx.loc[song_sfx['grade'].isin(['1.4.D']), 'grade'] = 'D'
song_sfx.loc[song_sfx['grade'].isin(['1.3.F', '2.3.F']), 'grade'] = 'F'


# In[28]:


df2 = song_sfx


# In[ ]:


# Create the dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    [
        html.H1("2조 대시보드 프로젝트", style={"textAlign": "center"}
               
               ),
        html.Div(
            [
                dcc.Graph(
                    id="graph1",
                    figure=fig1,
                    style={
                        "height": "25vh", 
                        "width": "23%", 
                        "float": "left",


       
                        'margin': '10px',
                        'display': 'inline-block',
                    
                    },
                ),
                dcc.Graph(
                    id="graph2",
                    figure=fig2,
                    style={
                        "height": "25vh", 
                        "width": "23%", 
                        "float": "left",
    
       
                
              
                        'margin': '10px',
                        'display': 'inline-block',
                    
                    },
                ),
                dcc.Graph(
                    id="graph3",
                    figure=fig3,
                    style={
                        "height": "25vh", 
                        "width": "23%", 
                        "float": "left",
  
          
                        'margin': '10px',
                        'display': 'inline-block',
                    
                    },
                ),
                dcc.Graph(
                    id="graph4",
                    figure=fig4,
                    style={
                        "height": "25vh", 
                        "width": "23%", 
                        "float": "left",
         
                
                        'margin': '10px',
                        'display': 'inline-block',
                    
                    },
                ),
            ],
            style={"width": "100%", "display": "flex", "flex-wrap": "wrap"},
            className='graph-container'
        ),
        html.Div([
                 dcc.Graph(
                    id="graph5",
                    figure=fig5,
                    style={
                        "height": "45vh", 
                        "width": "47.7%", 
                        "float": "left",
  
             
                        'margin': '10px',
                        'display': 'inline-block',
                    
                    },
                ),           
            
                html.Div([
                    dcc.Dropdown(
                        id='dropdown_for_practice',
                        options=[
                            {'label': 'Personal', 'value': 'person'},
                            {'label': 'smallBiz', 'value': 'small'},
                            {'label': 'middleBiz', 'value': 'middle'},
                            {'label': 'bigBiz', 'value': 'big'}
                        ],
                        value='data4'
                    ),
                    dcc.Graph(id='graph_with_dropdown',
                             style={
                             "height": "40vh"}
                    )
               ], 
               style={
               "height": "50vh", 
               "width": "47.5%", 
               "float": "left",
   
  
               'margin': '10px',
               'display': 'inline-block',
                    
                },
            
                className='six columns'),
        ],
         style={ "width": "100%", "display": "flex", "flex-wrap": "wrap"},
        ),
        
        
        html.Div([
            html.Div([
                html.Div([
                    html.H4("Music Type"),
                    dcc.Checklist(
                        id='checklist-music-type',
                        options=[{'label': 'Song', 'value': 'song'}, {'label': 'SFX', 'value': 'sfx'}],
                        value=['song', 'sfx'],
                        labelStyle={'display': 'block', 'margin-bottom': '10px'}
                    ),
                    html.H4("Is Free"),
                    dcc.RadioItems(
                        id='radio-is-free',
                        options=[{'label': 'Free', 'value': True}, {'label': 'Not Free', 'value': False}],
                        value=True,
                        labelStyle={'display': 'block', 'margin-bottom': '10px'}
                    ),
                    html.H4("Is Visible"),
                    dcc.RadioItems(
                        id='radio-is-visible',
                        options=[{'label': 'Visible', 'value': True}, {'label': 'Not Visible', 'value': False}],
                        value=True,
                        labelStyle={'display': 'block', 'margin-bottom': '10px'}
                    ),
                ], style={"width": "8%","margin-left": "8%"}),

                html.Div([
                    html.H4("Grades"),
                    dcc.Checklist(
                        id='checklist-grades',
                        options=[{'label': i, 'value': i} for i in ['F', 'D', 'C', 'B', 'A', 'S']],
                        value=['A', 'S'],
                        labelStyle={'display': 'block', 'margin-bottom': '10px'}
                    ),
                ], style={"width": "8%", "float": "left"}),

                html.Div([
                    html.Div([
                        dcc.Graph(id='histogram-graph')
                    ], style={"height": "80vh"})
                ], style={"width": "76%", "float": "left"})

            ], style={"display": "flex", "justify-content": "space-between"}),



            # 두번째 레이아웃
            html.Div([
                html.H4("Download Count"),
                dcc.Slider(
                    id='slider-download-count',
                    min=df2['download_count'].min(),
                    max=df2['download_count'].max(),
                    step=100,
                    value=0,
                    marks={i: str(i) for i in range(df2['download_count'].min(), df2['download_count'].max() + 1, 500)}
                ),
                html.H4("Play Count"),
                dcc.Slider(
                    id='slider-play-count',
                    min=df2['play_count'].min(),
                    max=df2['play_count'].max(),
                    step=100,
                    value=0,
                    marks={i: str(i) for i in range(df2['play_count'].min(), df2['play_count'].max() + 1, 1500)}
                )
            ], className='d-flex flex-wrap', style={"width": "80%", "margin": "0 auto", 'align-items': 'flex-start'}, )

        ],
   
        )
    
    
    
    
    
    
    
    ],


    style={
        "width": "80%",
        "background-color": '#F8F8F8',
        "font-family": "verdana",
        "color": "#333",
        "padding": '20px',
       
    },
)


def create_histogram(music_type, is_free, is_visible, download_count, play_count, grades):
    filtered_df = df2[(df2['music_type'].isin(music_type)) & (df2['is_free'] == is_free) & (df2['is_visible'] == is_visible) & (df2['download_count'] >= download_count) & (df2['play_count'] >= play_count) & (df2['grade'].isin(grades))]
    fig = px.histogram(filtered_df, x='created_at', nbins=50,
             color_discrete_sequence=['rgb(78,94,160)'])
    fig.update_layout(

    margin=dict(t=65, b=5, l=0, r=0),
    xaxis_title=None, yaxis_title=None,

    plot_bgcolor='rgba(0,0,0,0)'
)
    return fig


@app.callback(
              [Output('graph_with_dropdown', 'figure'), 
               Output('histogram-graph', 'figure')],
              
              
              [Input('dropdown_for_practice', 'value'),
               Input('checklist-music-type', 'value'),
               Input('radio-is-free', 'value'),
               Input('radio-is-visible', 'value'),
               Input('slider-download-count', 'value'),
               Input('slider-play-count', 'value'),
               Input('checklist-grades', 'value')]


)
def update_figure(selected_value, music_type, is_free, is_visible, download_count, play_count, grades):
    if selected_value == 'person':
        figA = fig6
        
    elif selected_value == 'small':
        figA = fig7
        
    elif selected_value == 'middle':
        figA = fig8
        
    else:
        figA = fig9
        
    figB = create_histogram(music_type, is_free, is_visible, download_count, play_count, grades)
    
    return figA, figB




if __name__ == "__main__":
    app.run_server(dev_tools_hot_reload=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




