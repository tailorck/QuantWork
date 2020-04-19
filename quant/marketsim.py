"""
MC2-P1: Market simulator.

Chirag Tailor
"""

import pandas as pd
import numpy as np
import os

from util import get_data, plot_data
from portfolio.analysis import get_portfolio_value, get_portfolio_stats, plot_normalized_data

def compute_portvals(start_date, end_date, orders_file, start_val):
    """Compute daily portfolio value given a sequence of orders in a CSV file.

    Parameters
    ----------
        start_date: first date to track
        end_date: last date to track
        orders_file: CSV file to read orders from
        start_val: total starting cash available

    Returns
    -------
        portvals: portfolio value for each trading day from start_date 
        to end_date (inclusive)
    """
    # TODO: Your code here
    
    # Import data from csv
    orders = pd.read_csv(orders_file, index_col='Date')

    # Ensure there are no orders outside of date range
    dates = pd.date_range(start_date, end_date)
    df_dates = pd.DataFrame(index=dates)
    orders = orders.join(df_dates, how='inner')
    
    # Extract symbols from orders
    symbols = orders['Symbol']
    symbols = list(set(symbols))

    # Create Prices and Trade DF. Update time to dates to exclude weekends
    df_prices = get_data(symbols, dates, False)
    df_prices = df_prices.dropna()
    df_prices['CASH'] = 1.0
    dates = df_prices.index
   
    zeros = np.zeros(shape=(len(dates), len(symbols)))
    df_trade = pd.DataFrame(zeros, index=dates, columns=symbols)
    df_trade['CASH'] = 0.0

    # Filling in the table holdings
    for index, order in orders.iterrows():
      d = index
      s = order[0]
      otype = order[1]
      shares = order[2]

      if otype == 'BUY':
        df_trade.ix[d, 'CASH'] -= df_prices.ix[d, s]*shares
        df_trade.ix[d, s] += shares
      else:
        df_trade.ix[d, 'CASH'] += df_prices.ix[d, s]*shares
        df_trade.ix[d, s] -= shares
   
    # Generate holdings by performing cumulative sum of trades DF
    df_trade.ix[0,-1] += start_val
    df_holdings = df_trade.cumsum()
    df_values = df_holdings*df_prices
    
    portvals = df_values.sum(axis=1)

    return portvals


def test_run(start_date, end_date, orders_file, start_val):
    """Driver function."""
  
    # Process orders
    portvals = compute_portvals(start_date, end_date, orders_file, start_val)

    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # if a DataFrame is returned select the first column to get a Series
    
    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    # Simulate a $SPX-only reference portfolio to get stats
    prices_SPY = get_data(['SPY'], pd.date_range(start_date, end_date))
    prices_SPY = prices_SPY[['SPY']]  # remove SPY
    portvals_SPY = get_portfolio_value(prices_SPY, [1.0])
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = get_portfolio_stats(portvals_SPY)

    # Compare portfolio against $SPY
    print "Data Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPY: {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPY: {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPY: {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPY: {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    # Plot computed daily portfolio value
    df_temp = pd.concat([portvals, prices_SPY['SPY']], keys=['Portfolio', 'SPY'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value and SPY")

if __name__ == "__main__":
  # Define input parameters
  '''
  start_date = '2011-01-05'
  end_date = '2011-01-20'
  orders_file = os.path.join("orders", "orders-short.csv")
  start_val = 1000000

  start_date = '2011-01-10'
  end_date = '2011-12-20'
  orders_file = os.path.join("orders", "orders.csv")
  start_val = 1000000

  start_date = '2011-01-14'
  end_date = '2011-12-14'
  orders_file = os.path.join("orders", "orders2.csv")
  start_val = 1000000
  '''
  start_date = '2007-12-31'
  end_date = '2009-12-31'
  orders_file = 'out.txt'
  start_val = 10000

  test_run(start_date, end_date, orders_file, start_val)
