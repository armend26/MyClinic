import datetime
from datetime import date, timedelta

def getDateList():
    datelist = []
    for dates in range(32):
        days_after = (date.today()+timedelta(days=dates+1))
        if days_after.weekday() == 5 or days_after.weekday() == 6:
            continue
        else:
            new_date = days_after.isoformat()
            datelist.append(new_date)
    return datelist 
 