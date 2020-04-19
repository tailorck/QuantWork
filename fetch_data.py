import os
import json
import logging
import sys
import argparse
import time
from datetime import datetime as dt

import requests
import pandas as pd
import holidays
from bs4 import BeautifulSoup
from tqdm import tqdm

YAHOO_OPTIONS_HTML = "https://finance.yahoo.com/quote/SPY/options"
TABLE_HEADERS = [
    "Contract Name",
    "Last Trade Date",
    "Strike",
    "Last Price",
    "Bid",
    "Ask",
    "Change",
    "% Change",
    "Volume",
    "Open Interest",
    "Implied Volatility"
]
TODAY = dt.now()
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logger.info('%s: %2dm %2.2fs' % (method.__name__, (te - ts)/60, (te - ts)%60))
        return result
    return timed


def ensure_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def create_folders(ticker, bucket):
    # ~/data
    ensure_folder(DATA_FOLDER)

    # ~/data/SPY
    ticker_folder = os.path.join(DATA_FOLDER, ticker)
    ensure_folder(ticker_folder)

    # ~/data/SPY/2020-03-01
    date = TODAY.strftime("%Y-%m-%d")
    date_folder = os.path.join(ticker_folder, date)
    ensure_folder(date_folder)

    # ~/data/SPY/2020-03-01/{open, mid, close}
    bucket_folder = os.path.join(date_folder, bucket)
    ensure_folder(bucket_folder)

    return bucket_folder


def write_to_disk(dataframe, path):
    dataframe.to_csv(path, index=False)


def fetch_options(ticker, bucket):
    folder = create_folders(ticker, bucket)

    data_html = requests.get(YAHOO_OPTIONS_HTML).content
    content = BeautifulSoup(data_html, "html.parser")

    try:
        calls, puts = content.find_all("table")
    except ValueError as exp:
        logger.error("Skipping {}: {}".format(ticker, exp))
        return
    
    call_values = []
    for row in calls.find_all("tr")[1:]:
        call_values.append([cell.text for cell in row])

    put_values = []
    for row in puts.find_all("tr")[1:]:
        put_values.append([cell.text for cell in row])

    call_df = pd.DataFrame(call_values, columns=TABLE_HEADERS)
    put_df = pd.DataFrame(call_values, columns=TABLE_HEADERS)

    write_to_disk(call_df, os.path.join(folder, 'calls.csv'))
    write_to_disk(put_df, os.path.join(folder, 'puts.csv'))


def get_cmdline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--ticker-list-file", help="A json file with a list of ticker symbols to parse", required=True, type=str)
    parser.add_argument("-b", "--bucket", help="The time of day", required=True, type=str)
    return parser.parse_args()


@timeit
def fetch_all_data(tickers, bucket):
    for ticker in tickers:
        fetch_options(ticker, bucket)
        time.sleep(1)


def main():
    us_holidays = holidays.UnitedStates()
    date = TODAY.strftime("%Y-%m-%d")

    if TODAY.weekday() in holidays.united_states.WEEKEND:
        logger.info("{} - Skipping weekends".format(date))
        sys.exit(1)

    if TODAY in us_holidays:
        logger.info("{} - Skipping due to holiday {}".format(date, us_holidays.get(date)))
        sys.exit(1)

    args = get_cmdline_args()

    try:
        with open(args.ticker_list_file, "r") as f:
            tickers = json.load(f)
    except IOError as exp:
        logger.error(exp)
        sys.exit(1)

    fetch_all_data(tickers, args.bucket)


if __name__ == "__main__":
    main()
