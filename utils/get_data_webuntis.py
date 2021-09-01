import webuntis
import sys


def get_webuntis(cred, start, end):
    data = {}

    s = webuntis.Session(
        username=cred["username"],
        password=cred["password"],
        server=cred["server"],
        school=cred["school"],
        useragent=cred["useragent"]
    ).login()

    old_stderr = sys.stderr
    sys.stderr = sys.stdout

    try:
        if "class" in cred:
            klasse = s.klassen().filter(name=cred["class"])[0]
            timetable = s.timetable(start=start, end=end, klasse=klasse)
        elif "surname" in cred and "fore_name" in cred:
            student = s.get_student(surname=cred["surname"], fore_name=cred["fore_name"]).id
            timetable = s.timetable(start=start, end=end, student=student)
        else:
            raise AttributeError("WebUntis is not configured correctly. Neither class nor surname&fore_name is configured.")

        timetable = sorted(timetable, key=lambda lesson: lesson.start)

        for lesson in timetable:
            if lesson.code != "cancelled":
                st = lesson.start.hour + lesson.start.minute / 60.0
                en = lesson.end.hour + lesson.end.minute / 60.0

                if lesson.start.weekday() in data:
                    data[lesson.start.weekday()] += [(st, en)]
                else:
                    data[lesson.start.weekday()] = [(st, en)]
    except:
        print("Start and End Date not in the same school year.")

    sys.stderr = old_stderr
    return data
