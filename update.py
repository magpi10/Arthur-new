import requests
import xml.etree.ElementTree as ET
import datetime
import search


def update_xml(url):
    r = requests.get(url)
    open("iss.xml", "wb").write(r.content)


def update_next_pass():
    iss = ET.parse("iss.xml")
    root = iss.getroot()

    dates = []
    durations = []

    for x in root[0]:
        for y in x:
            if y.tag == "description":
                date = search.find_date(y.text)
                dates.append(date)
                duration = search.find_duration(y.text)
                durations.append(duration)

    now = datetime.datetime.now()

    next_pass = ""
    next_pass_duration = 0

    for i in range(len(dates)):
        if dates[i] > now:
            next_pass = dates[i]
            next_pass_duration = durations[i]
            break

    return [next_pass, next_pass_duration]
