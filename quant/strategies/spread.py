import pandas as pd
import numpy as np

import yfinance as yf



def get_historical_volatility(prices, period=90):
    prices = prices[-period:]
    returns = prices / prices.shift(1)
    returns = returns.dropna()
    return_rate = np.log(returns)
    return np.sqrt(252)*np.std(return_rate, ddof=1)


def forecast_standard_deviation(price, volatility, period):
    return price * volatility * np.sqrt(period/365)


def round_up(value, increment=5):
    pass


def round_down(value, increment=5):
    pass


def get_market_direction(sma1, sma2):
    # if the short-period sma is over the long-period sma, market is trending up.
    pass


def get_implied_volatility():
    pass


def get_history(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period='1y')
    

def main():
    history_df = get_history("SPY")
    current_price = history_df.Close[-1]
    HV = get_historical_volatility(history_df.Close)
    forecast_std = forecast_standard_deviation(current_price, HV, 30)
    over = current_price + forecast_std
    under = current_price - forecast_std

    if not get_implied_volatility(ticker) > 0.5:
        return

    print(under, current_price, over)


if __name__ == "__main__":
    main()
