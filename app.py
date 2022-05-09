import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
#import os


#os.chdir("/Users/Philip/Documents/NU Econ PhD/Scraper")
df = pd.read_csv("https://www.dropbox.com/s/vq24nrs4hkgygfe/dfMay-07.csv?dl=1")
options = df.columns

app = Dash(__name__)

app.layout = html.Div([
    #dcc.Graph(id = 'graph_dropdown'),
    dcc.Dropdown(
        id='xselection',
        options=options,
        value='Ancestry',
    ),
    dcc.Dropdown(
        id='x2selection',
        options=options,
        value='Height',
    ),
   dcc.Loading(dcc.Graph(id="graph"), type="graph") #'graph', 'cube', 'circle', 'dot' or 'default';
])

@app.callback(
  Output('graph', 'figure'),
    [Input('xselection', 'value'),Input('x2selection', 'value')])

def display_animated_graph(selection, newselection):
    means = df.groupby(['{}'.format(selection), '{}'.format(newselection),
                 'Date']).agg({'IUI Number': ['mean'], 'IUI ART Number': ['mean'],
                                'ICI Number': ['mean'], 'ICI ART Number': ['mean']}).reset_index()
    cols = ['{}'.format(selection), '{}'.format(newselection), 'Date','IUI Number',
        'IUI ART Number', 'ICI Number','ICI ART Number']
    means.columns = cols
    means = means.reset_index(col_level =1)
    animations =    px.bar(means, x = '{}'.format(selection), y = "IUI Number", 
               color = '{}'.format(newselection), animation_group = '{}'.format(selection),
               animation_frame = 'Date', barmode='group', range_y=[0,11])
    return animations




if __name__ == '__main__':
    app.run_server()
