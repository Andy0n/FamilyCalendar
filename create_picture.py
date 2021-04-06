import collections
import datetime
import itertools

from config import MATES, CALS
from utils.create_picture import create_picture, create_picture_magicmirror, create_picture_epaper
from utils.get_data_google import get_google
from utils.get_data_webuntis import get_webuntis
from utils.utils import *

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('Create a timetable picture')
    parser.add_argument('-wd', '--width', type=int, default=500,
                        help='width of the picture')
    parser.add_argument('-ht', '--height', type=int, default=800,
                        help='height of the picture')
    parser.add_argument('-l', '--linewidth', type=int, default=2,
                        help='width of the vertical lines')
    parser.add_argument('-m', '--mirror', action='store_true',
                        help='if the picture should be optimized for a smartmirror')
    parser.add_argument('-b', '--bitmap', '--epaper', action='store_true',
                        help='if the picture should be created as a bitmap (like an epaper would need it e.g.)')
    parser.add_argument('-n', '--names', action='store_true', default=False,
                        help='if names should be printed over the bars')
    parser.add_argument('-s', '--show', action='store_true',
                        help='if the picture should not be stored, but opened')
    parser.add_argument('-e', '--events', type=int, default=0,
                        help='how many events should be displayed below')
    parser.add_argument('-he', '--eventsheight', type=int, default=200,
                        help='the height of the section for the events, if they are displayed')
    parser.add_argument('-d', '--days', type=int, default=5,
                        help='days to foresee')
    parser.add_argument('-p', '--path', type=str, default='./time.png',
                        help='path+filename where the picture should be saved')
    parser.add_argument('-mr', '--margin', type=int, default=15,
                        help='max minutes between events that should be joined')
    args = parser.parse_args()

    start = datetime.datetime.utcnow().today().replace(hour=0, minute=0, second=0)
    end = (start + datetime.timedelta(days=args.days-1)).replace(hour=23, minute=59, second=59)
    wd = start.weekday()
    data = {}
    data_events = {}

    MARGIN_TO_JOIN = args.margin / 60.0

    for name in MATES:
        days = {}

        for i in range(wd, wd + 5):
            days[i % 7] = []

        if 'google' in MATES[name]:
            for calendarId in MATES[name]['google']:
                google_data, event_data = get_google(calendarId, MATES[name]['google'][calendarId], start, end,
                                                     event_count=args.events)
                join_data(days, google_data)
                if calendarId in CALS['google']:
                    join_data(data_events, event_data)

        if 'webuntis' in MATES[name]:
            join_data(days, get_webuntis(MATES[name]["webuntis"], start, end))

        join_events(days, MARGIN_TO_JOIN)
        data[name] = days

    data_events = dict(itertools.islice(collections.OrderedDict(sorted(data_events.items())).items(), args.events))
    img = None

    if args.mirror:
        img = create_picture_magicmirror(data, args.width, args.height, args.linewidth, args.names, args.events, args.eventsheight, data_events)
    elif args.bitmap:
        img = create_picture_epaper(data, args.width, args.height, args.linewidth, args.names, args.events, args.eventsheight, data_events)
    else:
        img = create_picture(data, args.width, args.height, args.linewidth, args.names, args.events, args.eventsheight, data_events)

    if args.show:
        img.show()
    else:
        img.save(args.path)
