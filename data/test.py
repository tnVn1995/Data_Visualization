#%%
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, RangeSlider, Dropdown
from bokeh.io import curdoc
from bokeh.layouts import row
from math import pi
import datetime as dt


#Read in the data

df = pd.read_csv('./data/stock_prices.csv')

#Filtering for apple stocks
df['shortened_date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')

df_apple = df[df['symbol'] == 'AAL']

df_apple.head()
#%%
#Create the ColumnDataSource object

data = ColumnDataSource(data = df_apple)


#* assign data to variables
inc = df.close > df.open
dec = df.open < df.close
w = 12*60*60*1000

#Creating the scatter plot 

plot = figure(title = 'Attribute selector application')
plot.diamond('x', 'y', source = data, color = 'red')


p = figure(x_axis_type="datetime", plot_width=1000, title = "MSFT Candlestick")
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3

p.segment('date', 'high', 'date', 'close', color="black", source=data_points)
p.vbar(df_apple.date[inc], w, df_apple.open[inc], df_apple.close[inc], fill_color="#D5E1DD", line_color="black")
p.vbar(df_apple.date[dec], w, df_apple.open[dec], df_apple.close[dec], fill_color="#F2583E", line_color="black")

#Creating the select widget

# select_widget = Select(options = ['low', 'volume'], value = 'low', title = 'Select a new y axis attribute')
range_slider = RangeSlider(start=0, end=10, value=(1,9), step=.1, title="Stuff")


#Define the callback function
def callback1(attr, old, new):
    
    points = range_slider.value

# def callback(attr, old, new):
    
#     if new == 'low':
        
#         data.data = {'x' : df_apple['high'], 'y': df_apple['low']}
        
#     else:
        
#         data.data = {'x' : df_apple['high'], 'y': df_apple['volume']}
        
# select_widget.on_change('value', callback)




#Add the layout to the application

layout = row(range_slider, p)

curdoc().add_root(layout)

#%%
from math import pi
import datetime
from datetime import date
import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import layout
from bokeh.io import curdoc
from typing import Tuple



from bokeh.models import ColumnDataSource, Select, DateRangeSlider, Dropdown
from bokeh.io import curdoc
from bokeh.layouts import row

# from bokeh.sampledata.stocks import MSFT

df = pd.read_csv('./data/stock_prices.csv')

#Filtering for apple stocks
df['shortened_date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')

df_apple = df.loc[(df['symbol'] == 'AAL') & (df['shortened_date'].dt.year == 2016),:]

data = ColumnDataSource(data = df_apple)

inc = df.close > df.open
dec = df.open > df.close
w = 12*60*60*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = "MSFT Candlestick")
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3

range_slider = DateRangeSlider(start=df['shortened_date'].min(), end=df['shortened_date'].max(), value=(date(2016,2,3),date(2016,3,3)), step=1, title="Date Range")
# def candle_plot(stock_range: Tuple[float,float], df : pd.DataFrame = df_apple):
#     df = df_apple[]
p.segment('shortened_date', 'high', 'shortened_date', 'low', color="black", source=data)
# p.vbar(data.shortened_date[inc], w, data.open[inc], data.close[inc], fill_color="#D5E1DD", line_color="black")
# p.vbar(data.shortened_date[dec], w, data.open[dec], data.close[dec], fill_color="#F2583E", line_color="black")

def callback(attr, old, new):
    points = range_slider.value
    date1, date2 = np.datetime64(points[0]), np.datetime64(points[1])
    data1 = df_apple.loc[(df_apple['shortened_date'] >= np.datetime64(date1))&(df_apple['shortened_date'] <= np.datetime64(date2))]
    # inc = data1.close > data1.open
    # dec = data1.open > data1.close
    data = {'shortened_date': data1.shortened_date  , 'high': data1.high , 'low': data1.low,
    }

range_slider.on_change('value', callback)
layout = row(slider_widget, plot)
curdoc().add_root(layout)
# output_file("candlestick.html", title="candlestick.py example")

# show(p)  # open a browser



# %%
