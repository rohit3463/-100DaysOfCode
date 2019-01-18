import pandas as pd
import numpy as np
import sys
import os
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, CategoricalColorMapper, HoverTool, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis
from bokeh.models.widgets import CheckboxGroup, CheckboxButtonGroup, RangeSlider, Slider, Tabs, TableColumn, DataTable, Select

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

from itertools import chain

def route_tab(flights):

	def make_dataset(origin, destination):

		subset = flights[(flights['dest'] == destination) & (flights['origin'] == origin)]

		carriers = list(set(subset['name']))

		xs = []
		ys = []
		label_dict = {}

		for i, carrier in enumerate(carriers):

			carrier_data = subset[subset['name'] == carrier]

			ys.append([i for _ in range(len(carrier_data))])
			xs.append(list(carrier_data['arr_delay']))

			label_dict[i] = carrier 


		xs = list(chain(*xs))
		ys = list(chain(*ys))

		new_src = ColumnDataSource(data = {'x':xs, 'y':ys})

		return new_src, label_dict

	def make_plot(src, origin, destination, label_dict):

		p = figure(plot_width = 800, plot_height = 400, x_axis_label = 'Delay (min)', y_axis_label = "",
			title = 'Arrival Delays for Flight from %s to %s' % (origin, destination))

		p.circle('x', 'y', source = src, alpha = 0.4, color = 'navy', size = 15)

		p.yaxis[0].ticker.desired_num_ticks = len(label_dict)

		p.yaxis.formatter = FuncTickFormatter(code = """ var labels = %s; return labels[tick];"""% label_dict)

		return p 

	def style(p):
		# Title 
		p.title.align = 'center'
		p.title.text_font_size = '20pt'
		p.title.text_font = 'serif'

		# Axis titles
		p.xaxis.axis_label_text_font_size = '14pt'
		p.xaxis.axis_label_text_font_style = 'bold'
		p.yaxis.axis_label_text_font_size = '14pt'
		p.yaxis.axis_label_text_font_style = 'bold'

		# Tick labels
		p.xaxis.major_label_text_font_size = '12pt'
		p.yaxis.major_label_text_font_size = '12pt'

		return p

	def update(attr, old, new):
		origin = origin_select.value
		destination = dest_select.value

		new_src, label_dict = make_dataset(origin, destination)

		if len(label_dict) == 0:
			p.title.text = 'No flights on Record from %s to %s' % (origin, destination)

		else:
			p.yaxis[0].ticker.desired_num_ticks = len(label_dict)
			p.yaxis.formatter = FuncTickFormatter(code = """ var labels = %s; return labels[tick];""" % label_dict)

			p.title.text = 'Arrival Delays for Flights from %s to %s' % (origin, destination)


		src.data.update(new_src.data)


	origins = list(set(flights['origin']))
	dests = list(set(flights['dest']))

	origin_select = Select(title ='Origin', value = 'JFK', options = origins)
	origin_select.on_change('value', update)

	dest_select = Select(title = 'Destination', value = 'MIA', options = dests)
	dest_select.on_change('value', update)

	initial_origin = origin_select.value
	intial_dest = dest_select.value

	src, label_dict = make_dataset(initial_origin, intial_dest)

	p = make_plot(src, initial_origin, intial_dest, label_dict)

	p = style(p)

	controls = WidgetBox(origin_select, dest_select)
	layout = row(controls, p)

	tab = Panel(child = layout, title = 'Route Details')

	return tab 
