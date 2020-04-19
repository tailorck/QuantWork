"""
  MC2-P2: My Strategy

  Chirag Tailor
  902646034
  November 4th, 2015
  cs7646
"""
import pandas as pd
import matplotlib.pyplot as plt
import marketsim
from util import get_data
from indicators.Bollinger import calculate_bollinger
from indicators.RSI import calculate_rsi
from indicators.MACD import calculate_macd

def find_trades(df):
  """
  Calculates entry and exits points for my strategy
  
  My Strategy is better explained in my report
  """

  # Gather all the data I will need. 
  # I use default values for all technical indicators
  rsi = calculate_rsi(df)
  macd = calculate_macd(df)
  sma = pd.rolling_mean(df, 20)
  
  green = []
  red = []
  black = []

  r = [0, 0, 0]
  g = [0, 0, 0]
  gs = 0
  rs = 0
  entry = 0 
  for (i_prev, i_curr) in zip(df.index, df.index[1:]):
    curr_price = df.ix[i_curr, 0]
    prev_price = df.ix[i_prev, 0]
  
    if g[0] != 1 and sma.ix[i_prev, 0] < sma.ix[i_curr, 0]:
      g[0] = 1
    elif r[0] != 1 and sma.ix[i_prev, 0] > sma.ix[i_curr, 0]:
      r[0] = 1
    if g[1] != 1 and macd.ix[i_prev, 0] < 0 and macd.ix[i_curr, 0] > 0:
      g[1] = 1
    elif r[1] != 1 and macd.ix[i_prev, 0] > 0 and macd.ix[i_curr, 0] < 0:
      r[1] = 1
    if g[2] != 1 and (rsi.ix[i_prev, 0] < 30 and rsi.ix[i_curr, 0] > 30) or (rsi.ix[i_prev, 0] < 50 and rsi.ix[i_curr, 0] > 50):
      g[2] = 1
    elif r[2] != 1 and (macd.ix[i_prev, 0] > 70 and macd.ix[i_curr, 0] < 70) or (rsi.ix[i_prev, 0] > 50 and rsi.ix[i_curr, 0] < 50):
      r[2] = 1

    if not entry and sum(g) == 3:
      green.append((i_curr, curr_price))
      entry = 1
      r = [0, 0, 0]
    elif not entry and sum(r) == 3:
      red.append((i_curr, curr_price))
      entry = 1
      g = [0, 0, 0]

    if entry and sum(g) == 3:
      entry_price = green[-1][1]
      if curr_price > entry_price*1.2 or curr_price < entry_price*0.99:
        black.append((i_curr, curr_price))
        g = [0, 0, 0]
        entry = 0
    elif entry and sum(r) == 3:
      entry_price = red[-1][1]
      if curr_price < entry_price*0.8 or curr_price > entry_price*1.01:
        black.append((i_curr, curr_price))
        r = [0, 0, 0]
        entry = 0

  return green, red, black

def plot_charts(df):
  sma, upper, lower = calculate_bollinger(df)
  rsi = calculate_rsi(df)
  macd = calculate_macd(df)
  
  green, red, black = find_trades(df)
  
  ax1 = plt.subplot2grid((6,6), (0,0), colspan=6, rowspan=1)
  ax1.plot(df.index, rsi, 'k-')
  ax1.set_ylabel('RSI')
  ax1.axhline(y=30, color='black')
  ax1.axhline(y=70, color='black')
  ax1.axhline(y=50, color='black')
  ax1.axes.get_xaxis().set_visible(False)
  ax2 = plt.subplot2grid((6,6), (1,0), colspan=6, rowspan=4, sharex=ax1)
  ax2.plot(df.index, df, 'k-', label='IBM')
  ax2.plot(df.index, upper, 'b-')
  ax2.plot(df.index, lower, 'b-')
  ax2.plot(df.index, sma, 'r-')
  ax2.set_ylabel("Price")
  ax2.axes.get_xaxis().set_visible(False)
  ax3 = plt.subplot2grid((6,6), (5,0), colspan=6, rowspan=1, sharex=ax1)
  ax3.plot(df.index, macd, 'g-')
  ax3.set_ylabel("MACD")
  ax3.axhline(y=0, color='black')
  for item in green:
    date = item[0]
    ax1.axvline(x = date, color='green')
    ax2.axvline(x = date, color='green')
    ax3.axvline(x = date, color='green')
  for item in red:
    date = item[0]
    ax1.axvline(x = date, color='red')
    ax2.axvline(x = date, color='red')
    ax3.axvline(x = date, color='red')
  for item in black:
    date = item[0]
    ax1.axvline(x = date, color='black')
    ax2.axvline(x = date, color='black')
    ax3.axvline(x = date, color='black')

  plt.show()

def create_orders(df_price, outfile):
  green, red, black = find_trades(df_price)
 
  stock = df_price.columns[0]
  
  green = [green[i][0] for i in range(len(green))]
  red = [red[i][0] for i in range(len(red))]
  black = [black[i][0] for i in range(len(black))]
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
  dates = pd.date_range(start_date, end_date)
  symbols = ['IBM']
  df = get_data(symbols, dates, False)
  df = df.dropna()
  orders_file = 'orders/out.txt' 
  
  plot_charts(df)
  create_orders(df, orders_file)
  marketsim.test_run(start_date, end_date, orders_file, 10000)

if __name__ == '__main__':
  main()
