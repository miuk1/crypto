from logging import exception
import sys
import time
from helpers import interval_to_ms, utcdate_to_milliseconds
from data_client import MarketData
import os
import pandas as pd


def get_earliest_timestamp(symbol, interval):
    """Get the earliest timestamp from specified interval
    :param symbol: ticker name
    :param interval: timeperiod of the candlestick

    :return:
        time in milliseconds
    """
    kline_params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1,
        'startTime': 0,
        'endTime': int(time.time() * 1000)
    }

    klines_data = MarketData(
        'https://api.binance.com/api/v3/klines', kline_params).getMarketData()
    print(klines_data)
    return klines_data[0][0]


def getKlines(start_date, end_date, ticker, timeperiod, limit=500):
    """Get Klines data for specified start date and end date, limit 500 per call
    :param start_date: starting date in UTC
    :param end_date: end date in utc
    :param ticker: name or symbol of the desired currency pair
    :param limit: default 500

    :return: 
        csv file with historical kline data saved to folder csv historical data
    """
    
    df = pd.DataFrame()
    output_data = []
    timeperiod_ms = interval_to_ms(timeperiod)
    start_ts = utcdate_to_milliseconds(start_date)

    # get first available timestamp for given timeperiod
    first_valid_timestamp = get_earliest_timestamp(
        symbol=ticker, interval=timeperiod)
    start_ts = max(start_ts, first_valid_timestamp)
    end_ts = utcdate_to_milliseconds(end_date)

    # iterator
    it = 0
    while True:
        kline = {
            'symbol': ticker,
            'startTime': start_ts,
            'endTime': end_ts,
            'interval': timeperiod,
            'limit': limit
        }

        klines_data = MarketData(
            'https://api.binance.com/api/v3/klines', kline).getMarketData()
        if not len(klines_data):
            break

        output_data += klines_data

        start_ts = klines_data[-1][0]

        it += 1

        if len(klines_data) < limit:
            break

        start_ts += timeperiod_ms

        if it % 3 == 0:
            time.sleep(1)

    df = pd.concat([df, pd.DataFrame(output_data)])
    filename = f'./csv_historical_data/Binance_data_{start_date}_to_{end_date}_{timeperiod}.csv'
    
    if os.path.exists("./csv_historical_data/" + filename ):
        os.remove("./csv_historical_data/" + filename)
    
    df.to_csv(filename)
    return print(f'{filename} file created!')


if __name__ == "__main__":
    # get specific ticker from input
    if len(sys.argv) < 1:
        raise ValueError(
            'Please provide ticker name, timeperiod (1m, 5m, 30m), start_date (eg. 1 Jan, 2021), end_date(eg. 2 Jan, 2021')

    print(f'Script Name is {sys.argv[0]}')
    ticker = sys.argv[1]
    timeperiod = sys.argv[2]

    #date in human readable formats
    start_date = sys.argv[3]
    end_date = sys.argv[4]

    print(
        f'Getting candlestick data for {ticker} of {timeperiod} from {start_date} to {end_date}')

    getKlines(start_date, end_date, ticker, timeperiod)
