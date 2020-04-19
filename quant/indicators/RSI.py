"""
  Chirag Tailor
  November 3rd, 2015
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import get_data

def calculate_rsi(df_price, days=14):
    """Computes the RSI line for graph

    Parameters
    ----------
    df_price: a filled dataframe of df_price w/o nan values
    days: window size for SMA and rolling standard deviation

    Returns
    -------
    rsi: trend of the relative strength index 
    """
    df_price = df_price.dropna()
    df_price['Gain'] = 0.0
    df_price['Loss'] = 0.0
    symbol = df_price.columns[0]
    for (i_prev, i_curr) in zip(df_price.index, df_price.index[1:]):
        curr_price = df_price.ix[i_curr, 0]
        prev_price = df_price.ix[i_prev, 0]
        if prev_price < curr_price:
          df_price['Gain'][i_curr] = curr_price - prev_price
        if prev_price > curr_price:
          df_price['Loss'][i_curr] = abs(curr_price - prev_price)
  
    df_price['Avg Gain'] = pd.rolling_mean(df_price['Gain'], days)
    df_price['Avg Loss'] = pd.rolling_mean(df_price['Loss'], days)
    for (i_prev, i_curr) in zip(df_price.index[days-1:], df_price.index[days:]):
        prev_avg_gain = df_price.loc[i_prev, 'Avg Gain']
        prev_avg_loss = df_price.loc[i_prev, 'Avg Loss']
        curr_gain = df_price.loc[i_curr, 'Gain']
        curr_loss = df_price.loc[i_curr, 'Loss']
        df_price['Avg Gain'][i_curr] = (prev_avg_gain*(days-1)+curr_gain)/days
        df_price['Avg Loss'][i_curr] = (prev_avg_loss*(days-1)+curr_loss)/days
  
    df_price['RS'] = df_price['Avg Gain']/df_price['Avg Loss']
    df_price['RSI'] = 100 - 100/(1+df_price['RS']) 

    df_ret = pd.DataFrame(df_price['RSI'])
    return df_ret

def plot_rsi(df_price, days=14):
    """Plots bollinger bands

    Parameters
    ----------
    df_price: a filled dataframe of df_price w/o nan values
    days: window size for SMA and rolling standard deviation

    Returns
    -------
    ax: handle to plot generated
    Plot of stock, SMA, and bollinger bands
    """

    df_price = df_price.dropna()

    # Retrieve data to be plotted
    rsi = calculate_rsi(df_price, days)
    #rsi = (rsi/25) - 2 
    sma = pd.rolling_mean(df_price, days)

    # Plot original data with SMA, Bollinger Bands, Entries, and Exits
    ax1 = plt.subplot2grid((5,5), (0,0), colspan=5, rowspan=4)
    ax1.plot(df_price.index, df_price, 'b-', label=df_price.columns[0])
    ax1.plot(df_price.index, sma, 'r-', label='SMA')
    ax1.axes.get_xaxis().set_visible(False)
    ax1.set_ylabel("Price")
    ax1.legend(loc="lower right")

    ax2 = plt.subplot2grid((5,5), (4,0), colspan=5, sharex=ax1)
    #ax2 = plt.subplot2grid((5,5), (0,0), colspan=5, rowspan=4)
    ax2.plot(df_price.index, rsi, color='black')
    ax2.axhline(y=30, color='black')
    ax2.axhline(y=70, color='black')
    ax2.set_xlabel("Date")
    #ax2.set_ylim([-1.5,1.5])
    plt.show()

def main(symbols, dates):
    df = get_data(symbols, dates, False)
    plot_rsi(df)

if __name__ == "__main__":
    symbols = ['IBM']
    dates = pd.date_range('2007-12-31', '2009-12-31')
    main(symbols, dates)
