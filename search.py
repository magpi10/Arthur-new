import re
import datetime

months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

time_codes = {
    "minute": 60,
    "minutes": 60,
}

delta = datetime.timedelta(hours=12)


def find_date(description):
    date = re.search("([A-Z])\w+ \d+. \d+", description).group()
    month = re.search("([A-Z])\w+", date).group()
    month = months[month]
    day = re.search("\d+", date).group()
    day = int(day)
    year = re.search("\d\d\d\d", date).group()
    year = int(year)

    time = re.search("([A-Z])\w+. \d+.\d+ \w+", description).group()
    hour = re.search("\d+", time).group()
    hour = int(hour)
    minute = re.findall("\d+", time)[1]
    minute = int(minute)
    ampm = re.search("([A-Z])\w+", time).group()

    if ampm == "pm":
        hour += datetime.timedelta(hours=12)

    new_date = datetime.datetime(year, month, day, hour, minute)
    return new_date


def find_duration(description):
    duration = re.search("\d+ ([a-z])\w+", description).group()
    time = int(re.search("\d+", duration).group())
    time_multiplier = time_codes[re.search("([a-z])\w+", duration).group()]

    return time * time_multiplier
