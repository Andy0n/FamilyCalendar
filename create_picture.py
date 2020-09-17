import datetime

from config import MATES
from utils.create_picture import create_picture, create_picture_magicmirror
from utils.get_data_google import get_google
from utils.get_data_webuntis import get_webuntis
from utils.utils import *

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('Create a timetable picture')
    parser.add_argument('-wd', '--width', type=int, help='width of the picture', default=500)
    parser.add_argument('-ht', '--height', type=int, help='height of the picture', default=800)
    parser.add_argument('-l', '--linewidth', type=int, help='width of the vertical lines', default=2)
    parser.add_argument('-m', '--mirror', action='store_true', help='if the picture should be optimized for a smartmirror')
    parser.add_argument('-n', '--names', action='store_true', help='if names should be printed over the bars', default= False)
    parser.add_argument('-s', '--show', action='store_true', help='if the picture should not be stored, but opened')
    parser.add_argument('-d', '--days', type=int, help='days to foresee', default=5)
    parser.add_argument('-p', '--path', type=str, help='path+filename where the picture should be saved', default='./time.png')
    parser.add_argument('-mr', '--margin', type=int, help='max minutes between events that should be joined', default=15)
    args = parser.parse_args()

    start = datetime.datetime.utcnow().today().replace(hour=0, minute=0, second=0)
    end = (start + datetime.timedelta(days=args.days-1)).replace(hour=23, minute=59, second=59)
    wd = start.weekday()
    data = {}

    MARGIN_TO_JOIN = args.margin / 60.0

    for name in MATES:
        days = {}

        for i in range(wd, wd + args.days):
            days[i % 7] = []

        if 'google' in MATES[name]:
            for calendarId in MATES[name]['google']:
                join_data(days, get_google(calendarId, MATES[name]['google'][calendarId], start, end))

        if 'webuntis' in MATES[name]:
            join_data(days, get_webuntis(MATES[name]["webuntis"], start, end))

        join_events(days, MARGIN_TO_JOIN)
        data[name] = days

    img = None

    if args.mirror:
        img = create_picture_magicmirror(data, args.width, args.height, args.linewidth, args.names)
    else:
        img = create_picture(data, args.width, args.height, args.linewidth, args.names)

    if args.show:
        img.show()
    else:
        img.save(args.path)
