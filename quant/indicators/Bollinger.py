"""
  Chirag Tailor
  November 3rd, 2015
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt

from util import get_data

def calculate_bollinger(df_price, days=20):
  """Computes bollinger bands

  Parameters
  ----------
    df_price: a filled dataframe of df_price w/o nan values
    days: window size for SMA and rolling standard deviation

  Returns
  -------
    sma: simple moving average of prices
    upper_band: upper bollinger band
    lower_band: lower bollinger band
  """

  # Compute bands and plot
  df_price = df_price.dropna()
  sma = pd.rolling_mean(df_price, days)
  rolling_std = pd.rolling_std(df_price, days)
  upper_band = sma + 2*rolling_std
  lower_band = sma - 2*rolling_std

  return sma, upper_band, lower_band

def find_entries_exits(df_price, days=20):
    """
    Parameters
    ----------
    df_price: a filled dataframe of df_price w/o nan values

    Returns
    -------
    Creates a file of orders 
    """
    df_price = df_price.dropna()

    df_sma, df_uband, df_lband = calculate_bollinger(df_price, days)

    green = []
    red = []
    black = []
    entry = 0

    for (i_prev, i_curr) in zip(df_price.index, df_price.index[1:]):
        prev_price = df_price.ix[i_prev, 0]
        curr_price = df_price.ix[i_curr, 0]
        prev_sma = df_sma.ix[i_prev, 0]
        curr_sma = df_sma.ix[i_curr, 0]
        prev_uband = df_uband.ix[i_prev, 0]
        curr_uband = df_uband.ix[i_curr, 0]
        prev_lband = df_lband.ix[i_prev, 0]
        curr_lband = df_lband.ix[i_curr, 0]

        if df_sma.ix[i_prev, 0]:
            if not entry and prev_price > prev_uband and curr_price < curr_uband:
                red.append(i_curr)
                entry = 1
            elif not entry and prev_price < prev_lband and curr_price > curr_lband:
                green.append(i_curr)
                entry = 1

            if entry and prev_price < prev_sma and curr_price > curr_sma:
                black.append(i_curr)
                entry = 0
            elif entry and prev_price > prev_sma and curr_price < curr_sma:
                black.append(i_curr)
                entry = 0

    return green, red, black

def plot_bollinger_bands(df_price, days=20):
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
    sma, upper_band, lower_band = calculate_bollinger(df_price, days)  
    #green, red, black = find_entries_exits(df_price, days)

    # Plot original data with SMA, Bollinger Bands, Entries, and Exits
    plt.figure()
    ax = plt.gca()
    ax.plot(df_price.index, df_price, 'b-', label=df_price.columns[0])
    ax.plot(df_price.index, sma, 'r-', label='SMA')
    ax.plot(df_price.index, upper_band, 'c-', label='Bollinger Bands')
    ax.plot(df_price.index, lower_band, 'c-', label='')
    '''
    for date in green:
        ax.axvline(x=date, color='green')
    for date in red:
        ax.axvline(x=date, color='red')
    for date in black:
        ax.axvline(x=date, color='black')
    '''
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    plt.show()

    return ax

def create_orders(df_price, outfile, days=20):
    green, red, black = find_entries_exits(df_price, days)

    stock = df_price.columns[0]
    orders = green + red + black
    orders = sorted(orders)
    buy = 0 
    sell = 0 
    with open(outfile, 'w+') as out:
        out.write('Date,Symbol,Order,Shares\n')
        for date in orders:
            if date in green:
                out.write('{},{},BUY,100\n'.format(date, stock))
                buy = 1
            elif date in red:
                out.write('{},{},SELL,100\n'.format(date, stock))
                sell = 1
            elif date in black and buy: 
                out.write('{},{},SELL,100\n'.format(date, stock))
                buy = 0
            elif date in black and sell:
                out.write('{},{},BUY,100\n'.format(date, stock)) 
                sell = 0

    return

def main():
    start_date = '2007-12-31'
    end_date = '2009-12-31'
    orders_file = 'out.txt'
    dates = pd.date_range(start_date, end_date)
    df = get_data(['IBM'], dates, False)
    plot_bollinger_bands(df)
    #create_orders(df, orders_file)
    #marketsim.test_run(start_date, end_date, orders_file, 10000) 

if __name__ == "__main__":
    main()
