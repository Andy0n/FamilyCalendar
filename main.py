import datetime

from config import mates
from create_picture import create_picture
from get_data_google import get_google
from get_data_webuntis import get_webuntis

if __name__ == '__main__':
    start = datetime.datetime.utcnow().today().replace(hour=0, minute=0, second=0)
    end = (start + datetime.timedelta(days=4)).replace(hour=23, minute=59, second=59)

    for mate in mates:
        if 'google' in mate:
            for calenderId in mates[mate]['google']:
                get_google(calenderId, mates[mate]['google'][calenderId], start, end)

        if 'webuntis' in mate:
            get_webuntis(mate["webuntis"], start, end)

    create_picture()
