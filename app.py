import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go

os.chdir("/Users/Philip/Documents/NU Econ PhD/Scraper")
df = pd.read_csv("dfMay-07.csv")
df = df.loc[:,~df.columns.str.startswith('IVF')]
options = df.columns
ycols = [cols for cols in df.columns if 'IUI'not in cols]
deps = ['IUI Number', 'IUI ART Number','ICI Number', 'ICI ART Number']
diff2 = [i for i in ycols if "ICI" not in i]
diff = [i for i in diff2 if "Unnamed: 0" not in i]



app = dash.Dash(__name__)

app.layout = html.Div([
    #dcc.Graph(id = 'graph_dropdown'),
    html.P("Select a feature:"),
    dcc.Dropdown(
        id='xselection',
        options=diff,
        value='Ancestry',
    ),
    html.P("Select a grouping:"),
    dcc.Dropdown(
        id='x2selection',
        options=diff,
        value='Eye Color',
    ),
    html.P("Select the Dependent Variable:"),
    dcc.Dropdown(
        id='yselection',
        options=deps,
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