import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
plotly.offline.init_notebook_mode()

timesData = pd.read_csv('timesData.csv')

df = timesData.loc[:100,:]

trace1 = go.Scatter(x = df.world_rank,
                    y = df.citations,
                    mode = "lines + marker",
                    name = 'citations',
                    marker = dict(color = 'rgba(156,127,255,0.8)'),
                    text = df.university_name
                    )
trace2 = go.Scatter(x = df.world_rank,
                    y = df.teaching,
                    mode = "lines",
                    name = 'teachings',
                    marker = dict(color = 'rgba(16,112,2,0.8)'),
                    text = df.university_name
                    )
data = [trace1, trace2]

layout = dict(title = 'Citation and Teaching vs World Rank of Top 100 Universities',
              xaxis = dict(title = 'World Rank',
                          ticklen = 5,
                          zeroline = False)
             )
fig = dict(data = data, layout = layout)

iplot(fig)

df2014 = timesData[timesData.year == 2014].iloc[:100,:]
df2015 = timesData[timesData.year == 2015].iloc[:100,:]
df2016 = timesData[timesData.year == 2016].iloc[:100,:]

trace1 = go.Scatter(x = df2014.world_rank,
					y = df2014.citations,
					mode = 'markers',
					name = '2014',
					marker = dict(color = 'rgba(255, 128, 255, 0.8)'),
					text = df2014.university_name)

trace2 = go.Scatter(
					x = df2015.world_rank,
					y = df2015.citations,
					mode = 'markers',
					name = '2015',
					marker  =dict(color = 'rgba(255, 128, 2, 0.8)'),
					text = df2015.university_name)

trace3 = go.Scatter(
					x = df2016.world_rank,
					y = df2016.citations,
					mode = 'markers',
					name = '2016',
					marker = dict(color = 'rgba(0, 255, 200, 0.8)'),
					text = df2016.university_name)

data = [trace1, trace2, trace3]

layout = dict(title = "Citation vs world rank of Top 100 Universities",
			  xaxis = dict(title = 'World Rank', ticklen = 5, zeroline = False),
			  yaxis = dict(title = 'Citation', ticklen = 5, zeroline = False)
			  )
fig = dict(data = data, layout = layout)
iplot(fig)


df2014 = timesData[timesData.year == 2014].iloc[:3,:]

trace1 = go.Bar(
				x = df2014.university_name,
				y = df2014.citations,
				name = dict(color = 'rgba(255, 174, 255, 0.5)',
							line = dict(color = 'rgb(0,0,0)', width = 1.5)),
				text = df2014.country)

trace2 = go.Bar(
				x = df2014.university_name,
				y = df2014.teaching,
				name = "teaching",
				marker = dict(color = 'rgba(255, 255, 128, 0.5)',
							  line = dict(color = 'rgb(0,0,0)', width = 1.5)),
				text = df2014.country)

data = [trace1, trace2]

layout = go.Layout(barmode = "group")

fig = go.Figure(data = data, layout = layout)

ipllot(fig)



