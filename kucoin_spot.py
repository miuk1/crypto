import sys
import os
import time
import pandas as pd
from data_client import MarketData
from datetime import datetime, timedelta
from helpers import utcdate_to_seconds, interval_to_ms


def get_earliest_timestamp(symbol, interval):
    """Get the earliest timestamp from specified interval
    :param symbol: ticker name
    :param interval: timeperiod of the candlestick

    :return:
        time in milliseconds
    """
    kline_params = {
        'symbol': symbol,
        'type': interval,
        'limit': 1,
        'startTime': 0,
        'endTime': int(time.time() * 1000)
    }

    klines_data = MarketData(
        'https://api.kucoin.com/api/v1/market/candles', kline_params).getMarketData()
    return klines_data.get('data')[0][0]



def getTickers():
    # get list of all tickers from KuCoin Exchange
    tickers = []
    ticker_list = MarketData("https://api.kucoin.com/api/v1/market/allTickers",
                            {}).getMarketData()['data'].get('ticker')
    for ticker in ticker_list:
        tickers.append(ticker.get('symbol'))
    return tickers


def getKlines(start_date, end_date, ticker, timeperiod, limit=500):
    df = pd.DataFrame()

    output_data = []
    print(timeperiod)
    timeperiod_ms = interval_to_ms(timeperiod)

    # get first available timestamp for given timeperiod
    first_valid_timestamp = int(get_earliest_timestamp(
        symbol=ticker, interval=timeperiod))

    start_ts = utcdate_to_seconds(start_date)

    start_ts = max(start_ts, first_valid_timestamp)
    end_ts = utcdate_to_seconds(end_date) 

    print(end_ts)

    # iterator
    it = 0
    while True:
        kline = {
            'symbol': ticker,
            'startTime': start_ts,
            'endTime': end_ts,
            'type': timeperiod,
            'limit': limit
        }

        klines_data = MarketData(
            'https://api.kucoin.com/api/v1/market/candles', kline).getMarketData().get('data')

        if not len(klines_data):
            break

        output_data += klines_data
        start_ts = int(klines_data[-1][0])
        
        it += 1
        
        if len(klines_data) < limit:
            break
        
        start_ts = start_ts + (timeperiod_ms/1000) 
        print(start_ts)
        if it % 3 == 0:
            time.sleep(1)

    df = pd.concat([df, pd.DataFrame(output_data)])
    filename = f'./csv_historical_data/Kucoin_data_{start_date}_to_{end_date}_{timeperiod}.csv'
    
    if os.path.exists("./csv_historical_data/" + filename ):
        os.remove("./csv_historical_data/" + filename)
    
    df.to_csv(filename)
    return print(f'{filename} file created!')



if __name__ == "__main__":
    # get specific ticker from input
    if len(sys.argv) < 1:
        raise ValueError(
            'Please provide ticker name, timeperiod (1min, 5min, 30min), start_date (eg. 1 Jan, 2021), end_date(eg. 2 Jan, 2021')

    print(f'Script Name is {sys.argv[0]}')
    ticker = sys.argv[1]
    timeperiod = sys.argv[2]

    start_date = sys.argv[3]
    end_date = sys.argv[4]

    print(
        f'Getting candlestick data for {ticker} of {timeperiod} from {start_date} to {end_date}')

    getKlines(start_date, end_date, ticker, timeperiod)