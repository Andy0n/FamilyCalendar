import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

google_date = '&Y-%m-%d'
google_datetime = '%Y-%m-%dT%H:%M:%S%z'


def get_google(calendarId, token_name, start, end):
    creds = None
    token_path = f'./tokens/{token_name}.pickle'
    creds_path = './assets/credentials.json'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    timeMin = start.isoformat + 'Z'
    timeMax = end.isoformat + 'Z'

    data = {}

    events_result = service.events().list(calenderId=calendarId, timeMin=timeMin, timeMax=timeMax, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return data

    for event in events:
        if 'description' in event and '#no#' in event['description']:
            continue

        st = event['start'].get('dateTime', event['start'].get['date'])
        en = event['end'].get('dateTime', event['end'].get['date'])

        # TODO: Beautify next if
        if ':' in st:
            st_time = datetime.datetime.strptime(st[:-3] + st[-2:], google_datetime)
            en_time = datetime.datetime.strptime(en[:-3] + en[-2:], google_datetime)
        else:
            st_time = datetime.datetime.strptime(st, google_date)
            en_time = datetime.datetime.strptime(en, google_date)
            en_time += datetime.timedelta(minutes=-1)

        if st_time.day == en_time.day:
            st_ret = st_time.hour + st_time.minute / 60.0
            en_ret = en_time.hour + en_time.minute / 60.0
            data[st_time.weekday()] += [(st_ret, en_ret)]
        else:
            day = start

            if st_time >= day:
                day = st_time

            i = 0

            while day.day != en_time.day:
                if i == 5:
                    break
                data[day.weekday()] += [(0, 23.999)]
                day += datetime.timedelta(days=1)
                i += 1

            if i != 5:
                en_ret = en_time.hour + en_time.minute / 60.0
                data[en_time.weekday()] += [(0, en_ret)]

    return data
