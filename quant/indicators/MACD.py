import pandas as pd
import matplotlib.pyplot as plt
import sys
from util import get_data

def calculate_macd(df_price, slow=12, fast=26, signal=9):
    df_price = df_price.dropna()
    macd_line = pd.ewma(df_price, span=slow) - pd.ewma(df_price, span=fast)
    signal = pd.ewma(macd_line, span=signal)
    macd = macd_line-signal
    macd.columns = ['MACD'] 

    return macd

def execute_macd_strategy(df_price, slow=12, fast=26, signal=9):
    macd = calculate_macd(df_price, slow, fast, signal)

    green = []
    red = []
    black = []
    entry = 0
    r = 0
    g = 0 
    maxim = 0
    minim = sys.maxint
    for (i_prev, i_curr, i_next) in zip(macd.index, macd.index[1:], macd.index[2:]):
        '''
          Transitioning at only cross points results in terrible ROI
          Figure out how to transition on peaks
          Go from transition to transition and keep track of max or min values in btwn
        '''
        if not entry and macd.ix[i_prev, 0] < 0 and macd.ix[i_curr, 0] > 0:
            green.append(i_curr)
            entry=1
            g = 1
        '''
        elif entry and macd.ix[i_prev, 0] < 0 and macd.ix[i_curr, 0] > 0:
          black.append(i_curr)
          green.append(i_curr)
        '''
        if not entry and macd.ix[i_prev, 0] > 0 and macd.ix[i_curr, 0] < 0:
            red.append(i_curr)
            entry=1
            r = 1 
        '''
        elif entry and macd.ix[i_prev, 0] > 0 and macd.ix[i_curr, 0] < 0:
          black.append(i_curr)
          red.append(i_curr)
          entry=1
         
        '''
        if entry and g and macd.ix[i_prev, 0] < macd.ix[i_curr, 0] > macd.ix[i_next, 0]:
            black.append(i_prev)
            entry=0
            g = 0
        if entry and r and macd.ix[i_prev, 0] > macd.ix[i_curr, 0] < macd.ix[i_next, 0]:
            black.append(i_prev)
            entry = 0
            r = 0

    return green, red, black

def plot_macd(df_price, slow=12, fast=26, signal=9):
    df_price = df_price.dropna()
    macd = calculate_macd(df_price, slow, fast, signal)
    #green, red, black = execute_macd_strategy(df_price, slow, fast, signal)

    macd = macd / max(abs(macd['IBM']))
    symbol = df_price.columns[0]
    ax1 = plt.subplot2grid((5,5), (0,0), colspan=5, rowspan=4)
    ax1.plot(df_price.index, df_price, 'b-', label=symbol)
    ax1.set_ylabel("Price")
    ax1.axes.get_xaxis().set_visible(False)

    ax2 = plt.subplot2grid((5,5), (4,0), colspan=5, sharex=ax1)
    ax2.plot(macd.index, macd, color='green')
    ax2.axhline(y=0, color='black')

    '''
    for date in green:
    ax1.axvline(x=date, color='green')
    ax2.axvline(x=date, color='green')
    for date in red:
    ax1.axvline(x=date, color='red')
    ax2.axvline(x=date, color='red')
    for date in black:
    ax1.axvline(x=date, color='black')
    ax2.axvline(x=date, color='black')
    ''' 
    plt.show()

def main():
    dates = pd.date_range('2007-12-31', '2009-12-31')
    symbols = ['IBM']
    df = get_data(symbols, dates, False)
    plot_macd(df)
    return

if __name__ == "__main__":
    main()
