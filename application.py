import pandas as pd
import networkx as nx
import numpy as np
import pickle
import plotly.graph_objs as go
import dash
import flask
import math
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


swt=pd.read_csv('Star Wars Interactions.csv')
back_image="url(https://www.ljmu.ac.uk/~/media/ljmu/news/starsedit.jpg?h=400&w=780&la=en)"

color={1:'purple',4:'red',5:'navy',6:'green',2:'brown',3:'orange',7:'yellow',8:'silver',9:'cyan',3.5:'skyblue',3.55:'darkgreen'}

with open('cdi.pkl', 'rb') as cdi:
        colors_dict = pickle.load(cdi)

film_dict={'phantom':'Episode 1: The Phantom Menace','clones':'Episode 2: Attack of the Clones',
           'sith':'Episode 3: Revenge of the Sith','hope':'Episode 4: A New Hope','empire':'Episode 5: The Empire Strikes Back',
          'jedi':'Episode 6: Return of the Jedi','awakens':'Episode 7: The Force Awakens',
           'last':'Episode 8: The Last Jedi','skywalker':'Episode 9: The Rise of Skywalker',
           'rogue':'Rogue One: A Star Wars Story','solo':'Solo: A Star Wars Story'}

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.layout=html.Div(style={'background-image':back_image},children=[
    html.Div(children=[
        html.H1('Star Wars Character Connections'),
        html.H2('Choose a film (or combination of films) to see which characters shared scenes.'),
        html.H2('Each node is a character and each edge is an interaction.'),
        html.H3('Hover over a node to see how many connections that character has.'),
        html.H3('Click on a node to see who they shared a scene with (appears underneath diagram).'),    
    ],
    style={'textAlign': 'center',
            'color':  '#FFFF00',
            'backgroundColor': 'rgba( 0, 0, 0, 0.8)'}     
    ),
    dcc.Dropdown(id='options',
            options=[{'label':film_dict[i],'value':i} for i in film_dict.keys()],
            placeholder='Select film(s)',
            multi=True,
            searchable=False,
            style={'textAlign':'center','backgroundColor':'rgba( 0, 0, 0, 0.8)'}
    ),
    html.Div(id='graph',children=[
        dcc.Graph(id='network',style={'width': '49%', 'display': 'inline-block','vertical-align':'top'}),
        html.Div(children=[
        html.H2('Debut Film',style={'color':'white','textAlign':'right'}),
        html.H2('A New Hope',style={'color':'red','textAlign':'right'}),
        html.H2('Empire Strikes Back',style={'color':'navy','textAlign':'right'}),
        html.H2('Return of the Jedi',style={'color':'green','textAlign':'right'}),
        html.H2('The Phantom Menace',style={'color':'purple','textAlign':'right'}),
        html.H2('Attack of the Clones',style={'color':'brown','textAlign':'right'}),
        html.H2('Revenge of the Sith',style={'color':'orange','textAlign':'right'}),
        html.H2('The Force Awakens',style={'color':'yellow','textAlign':'right'}),
        html.H2('Rogue One',style={'color':'skyblue','textAlign':'right'}),
        html.H2('The Last Jedi',style={'color':'silver','textAlign':'right'}),
        html.H2('Solo',style={'color':'darkgreen','textAlign':'right'}),
        html.H2('The Rise of Skywalker',style={'color':'cyan','textAlign':'right'})],
        style={'width':'49%','height': 800, 'display': 'inline-block','vertical-align':'top','backgroundColor':'rgba( 0, 0, 0, 0.8)','textAlign':'center'}),
    ],style={'display':'none'}),
    html.Div(id='connections',style={'textAlign': 'center',
                                     'color':  '#FFFF00',
                                     'backgroundColor': '#111111',
                                      'list-style': 'inside'} 
    )
]
)
@app.callback([Output('graph','style'),
               Output('network','figure')],
              [Input('options','value')])
def output(value):
    films=[]
    if 'skywalker' in value:
        films.append(9)
    if 'solo' in value:
        films.append(3.55)
    if 'last' in value:
        films.append(8)
    if 'rogue' in value:
        films.append(3.5)
    if 'awakens' in value:
        films.append(7)
    if 'sith' in value:
        films.append(3)
    if 'clones' in value:
        films.append(2)
    if 'phantom' in value:
        films.append(1)
    if 'jedi' in value:
        films.append(6)
    if 'empire' in value:
        films.append(5)
    if 'hope' in value:
        films.append(4)  
    G=nx.Graph()
    for film in films:    
        sw=swt[swt.Film==film]
        sw.reset_index(inplace=True,drop=True)
        for i in range(len(sw)):
            chars=sw.Characters[i].split(',')
            for c in chars:
                G.add_node(c,color=color[film])
        for i in range(len(sw)):
            chars=sw.Characters[i].split(',')

            n=len(chars)-1
            while n>=0:
                m=n-1
                while m>=0:
                    tup=(chars[n],chars[m])
                    try:
                        G.add_edge(chars[n],chars[m],color=color[film])
                    except:
                        tup=(chars[m],chars[n])
                        G.add_edge(chars[n],chars[m],color=color[film])
                    m-=1
                n-=1
    layt=nx.spring_layout(G,dim=3)
    #Add edges and nodes

    edges = G.edges()
    nodes=G.nodes()
    #Define layout of graph
    with open('G.pkl', 'wb') as Gn:
        pickle.dump(G, Gn)
    #Node labels
    labels=[]
    for i in G.nodes():
        labels.append(i)
    #Node colours
    colors=[]
    for i in G.nodes():
        colors.append(colors_dict[i])
    N=len(G.nodes())
    deg=[]
    for i in G.nodes():
        deg.append(G.degree(i))
    Xn=[layt[k][0] for k in layt]# x-coordinates of nodes
    Yn=[layt[k][1] for k in layt]# y-coordinates
    Zn=[layt[k][2] for k in layt]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in G.edges():
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]
    

    trace1=go.Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=dict(color='grey', width=2),
                   hoverinfo='none'
                   )

    trace2=go.Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers+text',
                   name='characters',
                   marker=dict(symbol='circle',
                                 size=6,
                                 color=colors,
                                 colorscale='Viridis'
                                 
                                 
                   ),
                   text=labels,
                   hoverinfo='text',
                   hovertext=deg
                   )

    axis=dict(showbackground=False,
              showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )

    layout = go.Layout(
             title="Network of coappearances of characters in Star Wars<br>{}(3D visualization)".format([film_dict[i] for i in value]),
             width=1150,
             height=800,
             paper_bgcolor='rgba(0,0,0,0.8)',
             plot_bgcolor='rgba(0,0,0,0.8)',
             font={'color':'white'},
             clickmode='event+select',
             showlegend=False,
             scene=dict(
                 xaxis=dict(axis),
                 yaxis=dict(axis),
                 zaxis=dict(axis),
            ),
         margin=dict(
            t=100
        ),
        hovermode='closest',
          )
    data=[trace1, trace2]
    fig=go.Figure(data=data, layout=layout)
    return {'display':True},fig

@app.callback(Output('connections','children'),
             [Input('network','clickData')])
def node_show(click):
    with open('G.pkl', 'rb') as Gn:
        G = pickle.load(Gn)
    node=click['points'][0]['text']
    connections=G.neighbors(node)
    count=len([n for n in connections])
    children=[html.H2('Character: {}'.format(node)),
              html.Br(),
              html.H2('Number of Connections: {}'.format(count)),
              html.Br(),
              html.H2('Shared a scene with:'),
              html.Br(),
              html.Ul([html.Li(x) for x in G.neighbors(click['points'][0]['text'])])]
    return children

    
application=app.server
if __name__ == '__main__':
    application.run(debug=False,port=8080)