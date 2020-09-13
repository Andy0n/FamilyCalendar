import datetime

from config import mates
from get_data_webuntis import get_webuntis

if __name__ == '__main__':
    start = datetime.datetime.utcnow().today().replace(hour=0, minute=0, second=0)
    end = (start + datetime.timedelta(days=4)).replace(hour=23, minute=59, second=59)

    for mate in mates:
        if 'google' in mate:
            pass
        if 'webuntis' in mate:
            get_webuntis(mate["webuntis"], start, end)
