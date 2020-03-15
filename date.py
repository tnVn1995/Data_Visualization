from math import pi
import datetime
from datetime import date
import pandas as pd
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import layout
from bokeh.io import curdoc
from typing import Tuple, List



from bokeh.models import ColumnDataSource, Select, DateRangeSlider, Dropdown
from bokeh.io import curdoc
from bokeh.layouts import row, column

df = pd.read_csv('./data/stock_prices.csv')
df['shortened_date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')

year = 2016
def get_data(*args, stock_name: str='AAL', year:int =year) -> pd.DataFrame:

    #* Filter out data of stock_name in year    
    data = df.loc[(df['symbol'] == stock_name) & (df['shortened_date'].dt.year == year),:]

    #* For callback function
    if args:
        date1, date2 = args[0]
        stock, stock_day = args[1]
        data1 = data.loc[(data['shortened_date'] >= np.datetime64(date1))&(data['shortened_date'] <= np.datetime64(date2))]
        inc = data1.close > data1.open
        dec = data1.open > data1.close
        stock.data = {'shortened_date': data1.shortened_date, 
                        'high': data1.high , 
                        'low': data1.low,
        }
        stock_day.data = {'inc': data1.shortened_date[inc],
                        'dec': data1.shortened_date[dec],
                        'open_inc': data1.open[inc],
                        'close_inc': data1.close[inc],
                        'open_dec': data1.open[dec],
                        'close_dec': data1.close[dec]
        }

    # Load pd.Dataframe into Columndatasource for streaming
    else:
        stock = ColumnDataSource(data = data)
        inc = data.close > data.open
        dec = data.open > data.close

        stock_day = ColumnDataSource(data = {'inc': data.shortened_date[inc],
                                            'dec': data.shortened_date[dec],
                                            'open_inc': data.open[inc],
                                            'close_inc': data.close[inc],
                                            'open_dec': data.open[dec],
                                            'close_dec': data.close[dec]})
    return data, stock, stock_day

def yeardata(year:int = year):
    unique_stocks = df['symbol'].unique()
    year_data = df.loc[df['shortened_date'].dt.year==year]
    return year_data, unique_stocks

#* Get data for year
year_data, unique_stocks = yeardata(year=year)


w = 12*60*60*1000 # half day in ms

range_slider = DateRangeSlider(start=year_data['shortened_date'].min(), end=year_data['shortened_date'].max(),
                                value=(date(2016,2,3),date(2016,3,3)), step=1, title="Date Range")


#Filtering for chosen stock
Select1 = Select(title='Compare:', value='AAL', options=list(unique_stocks))
Select2 = Select(title='To:', value='GD', options=list(unique_stocks))

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

plot = figure(title='Stock Prices', 
                x_axis_type="datetime", 
                tools=TOOLS, 
                plot_width=1000,
                y_axis_label='Price in $USD',
                x_axis_label='Date'
)
plot.xaxis.major_label_orientation = pi/4
plot.grid.grid_line_alpha=0.3

# def candle_plot(stock_range: Tuple[float,float], df : pd.DataFrame = df_apple):
#     df = df_apple[]
def candle_plot(*args, plot:figure=plot, stock_name: str='AAL', color='blue'):
    #* Get data
    if args:
        whole, stock, stock_day = get_data(*args, stock_name=stock_name, )
    else:
        whole, stock, stock_day = get_data(stock_name=stock_name)

    plot.segment('shortened_date', 'high', 'shortened_date', 'low', color="black", source=stock)
    plot.vbar('inc', w, 'open_inc', 'close_inc', fill_color="#D5E1DD", line_color="black",source=stock_day, legend_label=(f'Mean price of {stock_name}'))
    plot.vbar('dec', w, 'open_dec', 'close_dec', fill_color="#F2583E", line_color="black",source=stock_day, legend_label=(f'Mean price of {stock_name}'))

    stock_mean_val=whole[['high', 'low']].mean(axis=1)
    plot.line(whole['shortened_date'], stock_mean_val, 
                legend=('Mean price of ' + stock_name), muted_alpha=0.2,
                line_color=color, alpha=0.5)
    return stock, stock_day

stock1, stock1_day = candle_plot(plot=plot, stock_name='AAL',color='blue')
stock2, stock2_day = candle_plot(plot=plot, stock_name='GD',color='green')

def callback(attr, old, new):

    #* Get stock names from Select menu
    stock_name1 = Select1.value

    #* Get the dates from slider
    points = range_slider.value
    date1 = datetime.datetime.fromtimestamp(points[0] / 1000)
    date2 = datetime.datetime.fromtimestamp(points[1] / 1000)
    date1, date2 = np.datetime64(date1), np.datetime64(date2)
    candle_plot([date1, date2], [stock1, stock1_day], plot=plot, stock_name=stock_name1, color='blue')

    #* Get stock name 2
    stock_name2 = Select2.value
    candle_plot([date1, date2], [stock2, stock2_day], plot=plot, stock_name=stock_name2, color='blue')

range_slider.on_change('value', callback)
Select1.on_change('value', callback)
Select2.on_change('value', callback)

layout = row(column(Select1, Select2, range_slider), plot)

curdoc().add_root(layout)