import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv("https://www.dropbox.com/s/vq24nrs4hkgygfe/dfMay-07.csv?dl=1")
options = df.columns

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.P("Select a feature:"),
    dcc.Dropdown(
        id='xselection',
        options=options,
        value='Ancestry',
    ),
    html.P("Select a grouping:"),
    dcc.Dropdown(
        id='x2selection',
        options=options,
        value='Height',
    ),
    html.P("Select the Dependent Variable:"),
    dcc.Dropdown(
        id='yselection',
        options=['IUI Number','IUI ART Number','ICI Number','ICI ART Number'],
        value='Height',
    ),
   dcc.Loading(dcc.Graph(id="graph"), type="graph") #'graph', 'cube', 'circle', 'dot' or 'default';
])

@app.callback(
  Output('graph', 'figure'),
    [Input('xselection', 'value'),Input('x2selection', 'value'),Input('yselection', 'value')])

def display_animated_graph(selection, newselection, yselection):
    means = df.groupby(['{}'.format(selection), '{}'.format(newselection),
                 'Date']).agg({'{}'.format(yselection): ['mean']}).reset_index()
    cols = ['{}'.format(selection), '{}'.format(newselection), 'Date','{}'.format(yselection)]
    means.columns = cols
    means = means.reset_index(col_level =1)
    animations =    px.bar(means, x = '{}'.format(selection), y = '{}'.format(yselection), 
               color = '{}'.format(newselection), animation_group = '{}'.format(selection),
               animation_frame = 'Date', barmode='group', range_y=[0,11])
    return animations


if __name__ == '__main__':
    app.run_server()