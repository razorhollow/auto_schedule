#!Python3

#List Index Helper:
#[0] = job number
#[1] = customer with space first
#[2] = partnum
#[3] = description
#[4] = due date
#[5] = routing
#[6] = prioritydate

import csv, os, pprint
import datetime
import pandas

#number of days given to priority customer
priority_value = 7

orderfile = open('C://users//rrey0//MyPythonScripts//Scheduling//Exports//OPENJOBS_FAB.csv')
routingfile = open('C://users//rrey0//MyPythonScripts//Scheduling//Exports//OPENROUTING_FAB.csv')

orders = csv.reader(orderfile)
routing = csv.reader(routingfile, delimiter = ",")


orderdata = list(orders)
notrouted = []
priority_customers = [' CBRE ', ' DRESSER ', ' CORNING ', ' FRONTIER ']
#format list for date processing

    
for list in orderdata:
    jobnum = list[0]
    list[0] = jobnum.strip(" ")   
    datestring = list.pop()
    datestring = datestring.replace("'","")
    datelist = datestring.split('/')   
    for item in datelist:
        index = datelist.index(item)        
        datelist[index] = int(item)
    list.append(datetime.datetime.date((datetime.datetime(datelist[2],datelist[0],datelist[1]))))
    


job_routing = {}
#compile routing times for each job
for line in routing:
    for item in line:
        line[line.index(item)] = item.replace("'","")   
    jobnum = line[0]  
    totaltime = float(line[2])
    try:
        job_routing[jobnum] += totaltime
    except KeyError:
        job_routing[jobnum] = totaltime
#pprint.pprint(job_routing)

#combine data to form raw unsorted queue
for list in orderdata:
    try:
        list.append(round(job_routing[list[0]],1))
    except KeyError:
        print('Key Error')
        continue

#Assign priority date and alert if no routing
Prioritized = []
for list in orderdata:
    if len(list) == 6:
        if list[1] in priority_customers:
            prioritydate = list[4] - datetime.timedelta(days=priority_value)
            list.append(prioritydate)            
        else:
            prioritydate = list[4]
            list.append(prioritydate)
        Prioritized.append(list)
        
    #No Routing: Ommitted        
    elif len(list) == 5:
        notrouted.append(list[0])        
    

#build sorted stack
df = pandas.DataFrame(Prioritized)
df.columns = ['Job Number', 'Customer', 'Part Number', 'Description', 'Due Date', 'Routing', 'Priority Date']
df.sort_values(by='Priority Date')
stack = df.values.tolist()
pprint.pprint(stack)
df.to_csv('out.csv', encoding='utf-8')
print('The following jobs have no routing and will be ommitted from schedule: ')
pprint.pprint(notrouted)
        
        
       
