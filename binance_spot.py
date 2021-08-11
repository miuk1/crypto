from logging import exception
import sys
import time
import pandas as pd
import calendar
from datetime import datetime, timedelta
from data_client import MarketData


# datespan function to iterate through dates


def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta


def get_unix_ms_from_date(date):
    return int(calendar.timegm(date.timetuple()) * 1000 + date.microsecond / 1000)


def getKlines(start_date, end_date, ticker, timeperiod):
    # get list of days between the specified days
    df = pd.DataFrame()
    # for day in datespan(start_date, end_date, delta=timedelta(days=1)):
    #     # Candlestick (kline) parameters
    #     print(day)
    #     kline = {
    #         'symbol': ticker,
    #         'startTime': int(time.mktime(day.timetuple())),
    #         'endTime': int(time.mktime(end_date.timetuple())),
    #         'interval': timeperiod,
    #         'limit': 1000
    #     }

    #     print(kline)

    #     klines = MarketData('https://api.binance.com/api/v3/klines', kline)
    #     klines_data = klines.getMarketData()
    #     df = pd.concat([df, pd.DataFrame(klines_data)])
    #     # dont exceed request limits
    #     time.sleep(0.5)

    # current_time = 0
    # start_time = int(time.mktime(start_date.timetuple()))

    

    filename = f'Binance_data_{start_date.date()}_to_{end_date.date()}_{timeperiod}.csv'
    df.to_csv(filename)

    return print(f'{filename} file created!')


if __name__ == "__main__":
    # get specific ticker from input
    if len(sys.argv) < 1:
        raise ValueError(
            'Please provide ticker name, timeperiod (1m, 5m, 30m), start_date(mm/DD/YY), end_date(mm/DD/YY)')

    print(f'Script Name is {sys.argv[0]}')
    ticker = sys.argv[1]
    timeperiod = sys.argv[2]

    start_date = datetime.strptime(sys.argv[3], '%m/%d/%Y')
    end_date = datetime.strptime(
        sys.argv[4], '%m/%d/%Y') + timedelta(days=1) - timedelta(microseconds=1)

    print(
        f'Getting candlestick data for {ticker} of {timeperiod} from {start_date} to {end_date}')

    getKlines(start_date, end_date, ticker, timeperiod)
