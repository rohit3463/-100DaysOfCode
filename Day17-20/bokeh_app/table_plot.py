import numpy as np 
import pandas as pd 
import sys
import os
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def table_tab(flights):

	carrier_stats = flights.groupby('name', as_index = False)['arr_delay'].describe()
	carrier_stats['name'] = pd.Series(flights['name'].unique(), index = carrier_stats.index)

	carrier_stats = carrier_stats.rename(columns = {'name':'airline', 'count':'flights','50%':'median'})

	carrier_stats['mean'] = carrier_stats['mean'].round(2)
	carrer_src = ColumnDataSource(carrier_stats)

	table_columns = [TableColumn(field = 'airline', title = 'Airline'),
					 TableColumn(field = 'flights', title = 'Number of Flights'),
					 TableColumn(field = 'min', title = 'Min Delay'),
					 TableColumn(field = 'mean', title = 'Mean Delay'),
					 TableColumn(field = 'median', title = 'Median Delay'),
					 TableColumn(field = 'max', title = 'Max Delay')]

	carrier_table = DataTable(source = carrer_src, columns = table_columns, width = 1000)

	tab = Panel(child = carrier_table, title = 'Summary Table')

	return tab 