import re

import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message= re.split(pattern, data)[1:]
    date= re.findall(pattern, data)
    df = pd.DataFrame({"messages":message, "Dates": date})
    df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y, %H:%M - ')
    users = []
    messages = []
    for message in df['messages']:
        pat = re.split('([\w\W]+?):\s', message)
        if pat[1:]:
            users.append(pat[1])
            messages.append(" ".join(pat[2:]))
        else:
            users.append("Notification")
            messages.append(pat[0])

    df['users'] = users
    df['messages'] = messages
    df['date'] = df['Dates'].dt.date
    df['year'] = df['Dates'].dt.year
    df['month_num'] = df['Dates'].dt.month
    df['month'] = df['Dates'].dt.month_name()
    df['day'] = df['Dates'].dt.day_name()
    df['day_num'] = df['Dates'].dt.day
    df['hour'] = df['Dates'].dt.hour
    df['minute'] = df['Dates'].dt.minute
    periods = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            periods.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            periods.append(str('00') + "-" + str(hour + 1))
        else:
            periods.append(str(hour) + "-" + str(hour + 1))

    df['periods'] = periods
    return df
