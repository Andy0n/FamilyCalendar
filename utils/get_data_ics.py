from ics import Calendar, Event
import requests
import datetime
import pytz

utc = pytz.utc


def get_icalendar(url, start, end, event_count=0):
    c = Calendar(requests.get(url).text)
    e = list(c.timeline)
    data = {}
    data_events = {}

    for event in e:
        st = event.begin.replace(tzinfo=utc)
        en = event.end.replace(tzinfo=utc)

        if en < start:
            continue
        if st > end:
            return data, data_events

        print(st, en)

        if event_count > 0:
            if event.name:
                if st not in data_events:
                    data_events[st] = []
                data_events[st] += [event.name]
                event_count -= 1

        st_ret = st.hour + st.minute / 60.0
        en_ret = en.hour + en.minute / 60.0

        if st.day == en.day:
            if st.weekday() in data:
                data[st.weekday()] += [(st_ret, en_ret)]
            else:
                data[st.weekday()] = [(st_ret, en_ret)]
        else:
            day = start

            if st >= day:
                day = st

            i = 0

            while day.day != en.day:
                if i == 5:
                    break

                if day.weekday() in data:
                    data[day.weekday()] += [(0, 23.999)]
                else:
                    data[day.weekday()] = [(0, 23.999)]

                day += datetime.timedelta(days=1)
                i += 1

            if i != 5:
                en_ret = en.hour + en.minute / 60.0
                if en.weekday() in data:
                    data[en.weekday()] += [(0, en_ret)]
                else:
                    data[en.weekday()] = [(0, en_ret)]

    return data, data_events
