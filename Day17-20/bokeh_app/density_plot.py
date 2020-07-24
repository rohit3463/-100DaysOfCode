import pandas as pd 
import numpy as np 
import sys
import os
from scipy.stats import gaussian_kde
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import (ColumnDataSource, HoverTool, CategoricalColorMapper, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, TableColumn, DataTable, Select
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def density_tab(flights):

	def make_dataset(carrier_list, range_start, range_end, bandwidth):

		xs = []
		ys = []
		colors = []
		labels = []

		for i, carrier in enumerate(list(carrier_list)):

			subset  =flights[flights['name'] == carrier]

			subset = subset[(subset['arr_delay'] > range_start) & (subset['arr_delay'] < range_end)]


			kde = gaussian_kde(subset['arr_delay'], bw_method = bandwidth)

			x = np.linspace(range_start, range_end, 100)

			y = kde.pdf(x)

			xs.append(x)
			ys.append(y)
			colors.append(airline_colors[i])
			labels.append(carrier)

		new_src = ColumnDataSource(data = {'x': xs, 'y': ys, 'color': colors, 'label': labels})

		return new_src


	def make_plot(src):

		p = figure(plot_width = 700, plot_height = 700, title  ="Density Plot of Arrival Delays by Airline",
					x_axis_label = "Delay (min)", y_axis_label = "Density")

		p.multi_line('x', 'y', color = 'color', legend = 'label', line_width = 3, source = src)

		hover = HoverTool(tooltips = [('Carrier','@label'), ('Delay', '$x'), ('Density','$y')], line_policy = 'next')

		p.add_tools(hover)

		p = style(p)

		return p 

	def update(attr, old, new):

		carriers_to_plot = [carrier_selection.labels[i] for i in carrier_selection.active]

		if bandwidth_choose.active == []:
			bandwidth = None
		else:
			bandwidth = bandwidth_slect.value

		new_src = make_dataset(carriers_to_plot, range_start = range_select.value[0], range_end = range_select.value[1], bandwidth = bandwidth)

		src.data.update(new_src.data)

	def style(p):

		p.title.align  ='center'

		p.title.text_font_size = '20pt'
		p.title.text_font = 'serif'

		p.xaxis.axis_label_text_font_size = '14pt'
		p.xaxis.axis_label_text_font_style = 'bold'
		p.yaxis.axis_label_text_font_size = '14pt'
		p.yaxis.axis_label_text_font_style = 'bold'

		p.xaxis.major_label_text_font_size = '12pt'
		p.yaxis.major_label_text_font_size = '12pt'

		return p

	available_carriers = list(set(flights['name']))
	available_carriers.sort()

	airline_colors = list(Category20_16)
	print(airline_colors)
	airline_colors.sort()

	carrier_selection = CheckboxGroup(labels = available_carriers, active = [0,1])

	carrier_selection.on_change('active', update)

	range_select = RangeSlider(start = -60, end = 180, value = (-60, 120), step = 5, title = 'Range of Delays (min)')

	range_select.on_change('value', update)

	initial_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]

	bandwidth_select = Slider(start = 0.1, end = 5, step = 0.1, value = 0.5, title = 'Bandwidth for Density Plot')

	bandwidth_select.on_change('value', update)

	bandwidth_choose = CheckboxButtonGroup(labels = ['Choose Bandwidth (Else Auto)'], active = [])

	bandwidth_choose.on_change('active', update)

	src = make_dataset(initial_carriers, range_start = range_select.value[0], range_end = range_select.value[1], bandwidth = bandwidth_select.value)

	p = make_plot(src)

	#p = style(p)

	controls = WidgetBox(carrier_selection, range_select, bandwidth_select, bandwidth_choose)

	layout = row(controls, p)

	tab = Panel(child = layout, title = 'Density Plot')

	return tab
