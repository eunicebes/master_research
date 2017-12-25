import plotly.graph_objs as go
import plotly.offline as po
from plotly.graph_objs import *

def generate_bar_chart(input_list, chart_title):
    x_axis = []
    y_axis = []
    for item in input_list:
        x_axis.append(item[0])
        y_axis.append(item[1])
    data = [go.Bar(
                x = x_axis,
                y = y_axis
        )]

    layout = go.Layout(
        title = chart_title,
    )
    fig = go.Figure(data=data, layout=layout)
    po.iplot(fig, filename='basic-bar')
    
def generate_histogram(input_list, chart_title):
    data = [go.Histogram(x = input_list)]
    layout = go.Layout(
        title = chart_title,
    )
    fig = go.Figure(data=data, layout=layout)
    po.iplot(fig, filename='basic histogram')
    
def generate_stacked_histogram(input_list_1, input_list_2, chart_title):
    trace0 = go.Histogram(
        x=input_list_1
    )
    trace1 = go.Histogram(
        x=input_list_2
    )
    data = [trace0, trace1]
    layout = go.Layout(barmode='stack', title=chart_title)
    fig = go.Figure(data=data, layout=layout)

    po.iplot(fig, filename='stacked histogram')