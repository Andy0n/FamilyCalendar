

def join_data(data, data_to_add):
    if data_to_add:
        for day in data_to_add:
            if day not in data:
                data[day] = []
            data[day] += data_to_add[day]
        return data


def merge(events, margin_to_join):
    if not events:
        return []

    saved = list(events[0])

    for st, en in sorted([sorted(t) for t in events]):
        if st <= saved[1] + margin_to_join:
            saved[1] = max(saved[1], en)
        else:
            yield tuple(saved)
            saved[0] = st
            saved[1] = en

    yield tuple(saved)


def join_events(days, margin_to_join):
    for day in days:
        days[day] = list(merge(days[day], margin_to_join))
    return days