import collections
import datetime
import itertools

from config import MATES, CALS
from utils.create_picture import create_picture, create_picture_magicmirror
from utils.get_data_google import get_google
from utils.get_data_webuntis import get_webuntis
from utils.utils import *


if __name__ == '__main__':
    start = datetime.datetime.utcnow().today().replace(hour=0, minute=0, second=0)
    end = (start + datetime.timedelta(days=4)).replace(hour=23, minute=59, second=59)
    wd = start.weekday()
    data = {}
    data_events = {}

    anzahl_events = 10

    MARGIN_TO_JOIN = 15/60.0

    for name in MATES:
        days = {}

        for i in range(wd, wd+5):
            days[i % 7] = []

        if 'google' in MATES[name]:
            for calendarId in MATES[name]['google']:
                google_data, event_data = get_google(calendarId, MATES[name]['google'][calendarId], start, end, event_count=anzahl_events)
                join_data(days, google_data)
                if calendarId in CALS['google']:
                    join_data(data_events, event_data)

        if 'webuntis' in MATES[name]:
            join_data(days, get_webuntis(MATES[name]["webuntis"], start, end))

        join_events(days, MARGIN_TO_JOIN)
        data[name] = days

    # create_picture(data, 500, 800).show()
    data_events = dict(itertools.islice(collections.OrderedDict(sorted(data_events.items())).items(), anzahl_events))
    create_picture_magicmirror(data, 500, 800, events=anzahl_events, event_data=data_events).show()
