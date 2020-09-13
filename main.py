import datetime

from config import mates
from create_picture import create_picture
from get_data_google import get_google
from get_data_webuntis import get_webuntis


def join_data(data, data_to_add):
    for day in data_to_add:
        data[day] += data_to_add[day]
    return data


if __name__ == '__main__':
    start = datetime.datetime.utcnow().today().replace(hour=0, minute=0, second=0)
    end = (start + datetime.timedelta(days=4)).replace(hour=23, minute=59, second=59)
    wd = start.weekday()
    data = {}

    for mate in mates:
        days = {}

        for i in range(wd, wd+5):
            days[i % 7] = []

        if 'google' in mates[mate]:
            for calenderId in mates[mate]['google']:
                join_data(days, get_google(calenderId, mates[mate]['google'][calenderId], start, end))

        if 'webuntis' in mates[mate]:
            join_data(days, get_webuntis(mates[mate]["webuntis"], start, end))

        data[mate] = days

    print(data)

    create_picture()
