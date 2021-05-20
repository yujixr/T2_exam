import csv
import os
import time
from datetime import date

from requests_oauthlib import OAuth1Session


def get_next_event(filename, today):
    next_event = None
    with open(filename, "r") as f:
        for row in csv.reader(f):
            name = row[0]
            year = int(row[1])
            month = int(row[2])
            day = int(row[3])

            scheduled_date = date(year, month, day)
            if scheduled_date > today:
                next_event = [name, str((scheduled_date - today).days)]
                break
    return next_event

GITHUB_EVENT_NAME = os.getenv("GITHUB_EVENT_NAME")
status = ""

if GITHUB_EVENT_NAME == "workflow_dispatch_x":
    status = "This is for debugging. (" + str(time.time()) + ")"
else:
    FILE_DIR = os.getenv("FILE_DIR")
    exams_file = os.path.join("./", FILE_DIR, "exams.csv")
    events_file = os.path.join("./", FILE_DIR, "events.csv")

    today = date.today()
    next_exam = get_next_event(exams_file, today)
    next_event = get_next_event(events_file, today)

    if next_exam is not None:
        status += next_exam[0] + "まであと" + next_exam[1] + "日です。\n"
    if next_event is not None:
        status += next_event[0] + "まであと" + next_event[1] + "日です。\n"
print(status)

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

params = { "status": status }
res = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)
print(res.status_code, res.text)

if res.status_code != 200:
    exit(1)
