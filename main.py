import datetime

from config import MATES
from create_picture import create_picture
from get_data_google import get_google
from get_data_webuntis import get_webuntis


def join_data(data, data_to_add):
    for day in data_to_add:
        data[day] += data_to_add[day]
    return data


def merge(events):
    if not events:
        return []

    saved = list(events[0])

    for st, en in sorted([sorted(t) for t in events]):
        if st <= saved[1]:
            saved[1] = max(saved[1], en)
        else:
            yield tuple(saved)
            saved[0] = st
            saved[1] = en

    yield tuple(saved)


def join_events(days):
    for day in days:
        days[day] = list(merge(days[day]))
    return days


if __name__ == '__main__':
    start = datetime.datetime.utcnow().today().replace(hour=0, minute=0, second=0)
    end = (start + datetime.timedelta(days=4)).replace(hour=23, minute=59, second=59)
    wd = start.weekday()
    data = {}

    for name in MATES:
        days = {}

        for i in range(wd, wd+5):
            days[i % 7] = []

        if 'google' in MATES[name]:
            for calendarId in MATES[name]['google']:
                join_data(days, get_google(calendarId, MATES[name]['google'][calendarId], start, end))

        if 'webuntis' in MATES[name]:
            join_data(days, get_webuntis(MATES[name]["webuntis"], start, end))

        join_events(days)
        data[name] = days

    create_picture(data, 500, 800).show()
