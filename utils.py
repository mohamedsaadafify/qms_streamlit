from datetime import datetime, timedelta

WEEKDAYS = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

def today_yy():
    return datetime.now().strftime('%y')

# Add working days, skipping weekend (Sat=5, Sun=6 by default)
def add_working_days(start_date, days, weekend=(5,6)):
    d = start_date
    added = 0
    while added < days:
        d += timedelta(days=1)
        if d.weekday() not in weekend:
            added += 1
    return d
