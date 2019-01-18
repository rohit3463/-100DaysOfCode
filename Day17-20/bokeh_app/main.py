import pandas as pd
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from histogram_plot import histogram_tab
from density_plot import density_tab
from table_plot import table_tab
from map_plot import map_tab
from routes_plot import route_tab
from bokeh.sampledata.us_states import data as states 

flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'), index_col = 0).dropna()

map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'), header = [0,1], index_col=0)

tab1 = histogram_tab(flights)
tab2 = density_tab(flights)
tab3 = table_tab(flights)
tab4 = map_tab(map_data, states)
tab5 = route_tab(flights)

tabs = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5])

curdoc().add_root(tabs)