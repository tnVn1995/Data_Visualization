from math import pi
import datetime
from datetime import date
import pandas as pd
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import layout
from bokeh.io import curdoc
from typing import Tuple



from bokeh.models import ColumnDataSource, Select, DateRangeSlider, Dropdown
from bokeh.io import curdoc
from bokeh.layouts import row

# from bokeh.sampledata.stocks import MSFT

df = pd.read_csv('./Lesson07/Activity31/data/stock_prices.csv')

#Filtering for apple stocks
df['shortened_date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')

df_apple = df.loc[(df['symbol'] == 'AAL') & (df['shortened_date'].dt.year == 2016),:]

data = ColumnDataSource(data = df_apple)
inc = df_apple.close > df_apple.open
dec = df_apple.open > df_apple.close

data2 = ColumnDataSource(data = {'inc': df_apple.shortened_date[inc],
                                    'dec': df_apple.shortened_date[dec],
                                    'open_inc': df_apple.open[inc],
                                    'close_inc': df_apple.close[inc],
                                    'open_dec': df_apple.open[dec],
                                    'close_dec': df_apple.close[dec]})

w = 12*60*60*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = "MSFT Candlestick")
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3

range_slider = DateRangeSlider(start=df_apple['shortened_date'].min(), end=df_apple['shortened_date'].max(), value=(date(2016,2,3),date(2016,3,3)), step=1, title="Date Range")
# def candle_plot(stock_range: Tuple[float,float], df : pd.DataFrame = df_apple):
#     df = df_apple[]
p.segment('shortened_date', 'high', 'shortened_date', 'low', color="black", source=data)
p.vbar('inc', w, 'open_inc', 'close_inc', fill_color="#D5E1DD", line_color="black",source=data2)
p.vbar('dec', w, 'open_dec', 'close_dec', fill_color="#F2583E", line_color="black",source=data2)

def callback(attr, old, new):
    points = range_slider.value
    date1 = datetime.datetime.fromtimestamp(points[0] / 1000)
    date2 = datetime.datetime.fromtimestamp(points[1] / 1000)
    date1, date2 = np.datetime64(date1), np.datetime64(date2)
    data1 = df_apple.loc[(df_apple['shortened_date'] >= np.datetime64(date1))&(df_apple['shortened_date'] <= np.datetime64(date2))]
    inc = data1.close > data1.open
    dec = data1.open > data1.close
    data.data = {'shortened_date': data1.shortened_date, 
                    'high': data1.high , 
                    'low': data1.low,
    }
    data2.data = {'inc': data1.shortened_date[inc],
                    'dec': data1.shortened_date[dec],
                    'open_inc': data1.open[inc],
                    'close_inc': data1.close[inc],
                    'open_dec': data1.open[dec],
                    'close_dec': data1.close[dec]
    }

range_slider.on_change('value', callback)
layout = row(range_slider, p)

curdoc().add_root(layout)