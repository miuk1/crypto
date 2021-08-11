from logging import exception
import sys
import time
import pandas as pd
from data_client import MarketData
from datetime import date, datetime, timedelta

# datespan function to iterate through dates
def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

def getTickers():
    # get list of all tickers from KuCoin Exchange
    tickers = []
    ticker_list = MarketData("https://api.kucoin.com/api/v1/market/allTickers",
                            {}).getMarketData()['data'].get('ticker')
    for ticker in ticker_list:
        tickers.append(ticker.get('symbol'))
    return tickers


def getKlines(start_date, end_date, ticker, timeperiod):
    # get list of days between the specified days
    df = pd.DataFrame()
    for day in datespan(start_date, end_date, delta=timedelta(days=1)):
        # Candlestick (kline) parameters
        kline = {
            'symbol': ticker,
            'startAt': int(time.mktime(day.timetuple())),
            'endAt': int(time.mktime(end_date.timetuple())),
            'type': timeperiod
        }

        print(kline)

        klines = MarketData('https://api.kucoin.com/api/v1/market/candles', kline)
        klines_data = klines.getMarketData().get('data')
        df = pd.concat([df, pd.DataFrame(klines_data)])
        time.sleep(0.5)
    
    filename = f'Kucoin_data_{start_date.date()}_to_{end_date.date()}_{timeperiod}.csv'
    df.to_csv(filename)

    print(f'{filename} file created!')



if __name__ == "__main__":
    # get specific ticker from input
    if len(sys.argv) < 1:
        raise ValueError(
            'Please provide ticker name, timeperiod (1min, 5min, 30min), MM/DD/YY')

    print(f'Script Name is {sys.argv[0]}')
    ticker = sys.argv[1]
    timeperiod = sys.argv[2]

    start_date = datetime.strptime(sys.argv[3], '%m/%d/%Y')
    end_date = datetime.strptime(sys.argv[4], '%m/%d/%Y') + timedelta(days=1) - timedelta(microseconds=1)

    print(
        f'Getting candlestick data for {ticker} of {timeperiod} from {start_date} to {end_date}')

    getKlines(start_date, end_date, ticker, timeperiod)