import datetime
import pprint

fmt = '%m/%d/%y %H:%M'

active = {'Garan': ['15179-01', 0, datetime.datetime(2017, 5, 24, 9, 6, 0, 418859)],
 'Greg': ['15179-01', 0, datetime.datetime(2017, 5, 24, 9, 6, 0, 408831)],
 'Jamie': ['15296-16', 0, datetime.datetime(2018, 1, 31, 7, 54, 0, 403316)],
 'Jon': ['15179-01', 0, datetime.datetime(2017, 5, 25, 7, 36, 0, 425919)],
 'Kevin': ['14953-01', 0, datetime.datetime(2017, 6, 21, 14, 6, 0, 435252)]}

def whos_next():
    d = {}
    for key in active:
        d[key] = active[key][2]
        pprint.pprint(d)
    try:
        return min(d, key = d.get)
    except TypeError:
        print('your shit broke')

employee = whos_next()
print(employee)
