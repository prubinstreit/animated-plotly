{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "79edeae0-1bfe-427d-a83f-f6adb3735316",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import dash\n",
    "from dash import Dash, dcc, html, Input, Output\n",
    "import plotly.express as px\n",
    "import plotly.graph_objs as go\n",
    "#import os\n",
    "\n",
    "\n",
    "#os.chdir(\"/Users/Philip/Documents/NU Econ PhD/Scraper\")\n",
    "df = pd.read_csv(\"https://www.dropbox.com/s/vq24nrs4hkgygfe/dfMay-07.csv?dl=1\")\n",
    "options = df.columns\n",
    "\n",
    "app = dash.Dash(__name__)\n",
    "server = app.server\n",
    "app.layout = html.Div([\n",
    "    #dcc.Graph(id = 'graph_dropdown'),\n",
    "    dcc.Dropdown(\n",
    "        id='xselection',\n",
    "        options=options,\n",
    "        value='Ancestry',\n",
    "    ),\n",
    "    dcc.Dropdown(\n",
    "        id='x2selection',\n",
    "        options=options,\n",
    "        value='Height',\n",
    "    ),\n",
    "   dcc.Loading(dcc.Graph(id=\"graph\"), type=\"graph\") #'graph', 'cube', 'circle', 'dot' or 'default';\n",
    "])\n",
    "\n",
    "@app.callback(\n",
    "  Output('graph', 'figure'),\n",
    "    [Input('xselection', 'value'),Input('x2selection', 'value')])\n",
    "\n",
    "def display_animated_graph(selection, newselection):\n",
    "    means = df.groupby(['{}'.format(selection), '{}'.format(newselection),\n",
    "                 'Date']).agg({'IUI Number': ['mean'], 'IUI ART Number': ['mean'],\n",
    "                                'ICI Number': ['mean'], 'ICI ART Number': ['mean']}).reset_index()\n",
    "    cols = ['{}'.format(selection), '{}'.format(newselection), 'Date','IUI Number',\n",
    "        'IUI ART Number', 'ICI Number','ICI ART Number']\n",
    "    means.columns = cols\n",
    "    means = means.reset_index(col_level =1)\n",
    "    animations =    px.bar(means, x = '{}'.format(selection), y = \"IUI Number\", \n",
    "               color = '{}'.format(newselection), animation_group = '{}'.format(selection),\n",
    "               animation_frame = 'Date', barmode='group', range_y=[0,11])\n",
    "    return animations\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run_server()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
