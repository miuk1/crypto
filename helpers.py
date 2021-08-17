from datetime import datetime, timedelta
from calendar import calendar
import time
from typing import Dict, Optional

import dateparser
import pytz


# datespan function to iterate through dates
def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta


def get_unix_ms_from_date(date):
    return int(calendar.timegm(date.timetuple()) * 1000 + date.microsecond / 1000)


# interval to milliseconds
def interval_to_ms(timeperiod: str):
    interval_to_seconds_mapping: Dict[str, int] = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
        "min": 60,
        "hour": 60 * 60,
        "day": 24 * 60 * 60,
        "week": 7 * 24 * 60 * 60,
    }    
    try:
        if (timeperiod.find('min')) > -1 or (timeperiod.find('day')) > -1:
            return int(timeperiod[:-3]) * interval_to_seconds_mapping[timeperiod[-3]] * 1000
        
        elif (timeperiod.find('hour')) > -1 or (timeperiod.find('week')) > -1:
            return int(timeperiod[:-4]) * interval_to_seconds_mapping[timeperiod[-4]] * 1000

        else:    
            return int(timeperiod[:-1]) * interval_to_seconds_mapping[timeperiod[-1]] * 1000
   
    except (ValueError, KeyError):
        return None


def utcdate_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)



def utcdate_to_seconds(date_str: str) -> int:
    """Convert UTC date to seconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds())