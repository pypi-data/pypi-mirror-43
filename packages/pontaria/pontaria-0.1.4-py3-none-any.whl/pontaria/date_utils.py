import arrow
import datetime
from functools import reduce
TZ = 'America/Sao_Paulo'

def get_date():
    return arrow.now(TZ).shift()

def get_period():
    now = get_date()
    year = now.year
    before_21 = now.day <= 20
    month_date = now.shift(months=-1) if before_21 else now
    first_month_str = month_date.format("MMM", locale='pt')[:3].capitalize()
    second_month_str = month_date.shift(months=1).format("MMM", locale='pt')[:3].capitalize()

    return f'{21}-{first_month_str}{year} a {20}-{second_month_str}{year}'

def sum_hours(hours_in_str):
    times = []
    for time in hours_in_str:
        h, m = [int(x) for x in time[:5].split(':')]
        times.append(datetime.timedelta(hours=h, minutes=m))
    delta = reduce( lambda x,y: x + y, times)
    return (delta.days * 24 + delta.seconds / 3600)