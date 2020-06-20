import plotly.express as px
import dash
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import re
from getlyric import pull_lyric
from songs import songs
import time

# https://www.metrolyrics.com/thinking-about-you-lyrics-frank-ocean.html
app = dash.Dash(__name__,    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
server=app.server
app.layout = html.Div(style={'height':'95vh','width':'100vw','text-align':'center','backgroundColor':'#111111'},
children=[
    html.Div(
        children=
            [
                    html.P('Popular Examples-',style={'color':'white','font-family':'Verdana'}),
                    dcc.Dropdown(id='song-dropdown',
                        options=songs,
                        clearable=False,
                        value='https://www.metrolyrics.com/we-will-rock-you-lyrics-queen.html'),
                    html.P('Search Song by Name-',style={'color':'white','font-family':'Verdana'}),
                    dcc.Input(id='artist-name', value='',placeholder='Artist Name', type='text'),
                    dcc.Input(id='artist-song', value='',placeholder='Name of Song' ,type='text'),
                    html.Div(
                        children=[
                        html.P('Search Song by URL(Only MetroLyrics)-',style={'color':'white','font-family':'Verdana'}),
                        dcc.Input(id='song-url', value='',type='text',style={'width':'70%'})],style={'width':'100%'}),
                        html.Div(
                        dcc.RadioItems(id='stopword-choice',
                        options=[
                                {'label': 'Ignore Stopwords', 'value': 1 },
                                {'label': 'Show All', 'value': 0},
                                ],
                        value=1),style={'color':'white'})
                        ],style={'width':'60vh','padding':'10px','float':'left','text-align':'left'}),

    html.Div(style={'width':'60vh','float':'right'},children=[html.P('PlaceHolder')]),
    html.Div(children=[
        dcc.Graph(id="graph",responsive=True,style={'height':'100%','width':'100%'})
    ],style={'width':'70vh','height':'70vh','text-align':'left', 'display': 'inline-block'}),
])

@app.callback(
    Output('graph', 'figure'),
    [
     Input(component_id='song-url', component_property='value'),
     Input(component_id='stopword-choice', component_property='value')]
)
def update_graph(song_url,stopword_choice):
    url = song_url
    df = pull_lyric(url,stopword_choice)
    fig=go.Figure(layout=go.Layout(
        template='plotly_dark',
        xaxis =  {                                     
                    'ticks':'',
                    'zeroline':False,
                    'showticklabels':False,
                    'showline':False,
                    'showgrid':True
                  },
        yaxis = {                              
                'ticks':'',
                'zeroline':False,
                'showticklabels':False,
                'showline':False,
                'showgrid':True,


              }))

    fig.add_trace(
    go.Scattergl(
            x=df['x'],
            y=df['y'],
            text=df['words'],
            mode='markers',
            marker_symbol=1,
            marker_size=5,
            marker={'color':df['freq']},

    ))
    return fig



@app.callback(
    Output('song-url', 'value'),
    [
     Input(component_id='song-dropdown', component_property='value'),
     Input(component_id='artist-name', component_property='value'),
     Input(component_id='artist-song', component_property='value')]
)
def update_url_on_text(dropdown_url,artist_name,artist_song):
    if artist_name!='' and artist_song!='':
        time.sleep(0.5)
        url=f"https://www.metrolyrics.com/{artist_song.lower().replace(' ','-')}-lyrics-{artist_name.lower().replace(' ','-')}.html"
    else:
        url=dropdown_url
    return url

@app.callback(
    Output('artist-song','value'),
    [
     Input(component_id='song-dropdown', component_property='value')
     ]
)
def clearsearchsong(value):
    if value!=None:
        return ''

@app.callback(
    Output('artist-name','value'),
    [
     Input(component_id='song-dropdown', component_property='value')
     ]
)
def clearsearchname(value):
    if value!=None:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
