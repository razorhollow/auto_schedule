import datetime
import csv
import pprint
import pandas

#f = open("schedule_{}".format(datetime.datetime.now().strftime('%m_%d_%y')), "a+")
#f.write("Jobs Currently In Process:\n")

fmt = '%m/%d/%y %H:%M'
employees = ['Garan', 'Jamie', 'Jon', 'Kevin', 'Greg']
#builds in a buffer to account for efficiency
efficiency = .7
eff_rate = 2- efficiency

active = {}

#dict of employee and estimated finish datetime of current job
def currentjob():
    for employee in employees:
        active[employee] = []
        current_job = input('What Job is {} currently on? >  '.format(employee))            
        active[employee].append(current_job)        
        hrs_remaining = input('How many hours do they have left?')
        active[employee].append(float(hrs_remaining))
    print (active)

#loop through active jobs and see if any in queue
#if so, remove from queue
def stack_purge():
    for key in active:
        jobnum = active[key][0]
        for list in stack:
            if jobnum in list:
                del stack[stack.index(list)]
                print('{} has been started, removing from stack...'.format(jobnum))
                input('Press Enter to Continue. ')

#function to determine finish date of a job, given start date and routed time
def count_forward(start, routed_time):
    running_time = routed_time
    running_date = start
    while running_time:
        
        routing = running_time * eff_rate
        end_day = start.replace(hour=15, minute=30, second=0)
        td = end_day - start
        tr = round(td.seconds/3600, 1)

        if tr > routing:
                    return running_date + datetime.timedelta(hours=routing)
                    
               
        else:
                              
            running_time -= tr
            if running_date.weekday() < 3:
                running_date += datetime.timedelta(days=1)
            else:
                running_date += datetime.timedelta(days=3)
            running_date = running_date.replace(hour=7, minute=0, second=0)
                
        

#collects input on who is working on what, how much time is left, determines finish date
def initialize():
    print('Employee  |  Job  |  Expected Finish')
    print('-'*20)
    for key in active:
        active[key].append(datetime.datetime.now())
        active[key][1] = active[key][1] * eff_rate
        while active[key][1]:
            routing = active[key][1]
            end_day = active[key][2].replace(hour=15, minute=30, second=0)
            td = end_day - active[key][2]
            tr = round(td.seconds/3600, 1)
           
            if tr > routing:
                    active[key][2] = active[key][2] + datetime.timedelta(hours=routing)
                    active[key][1] = 0
               
            else:
                              
                active[key][1] -= tr
                if active[key][2].weekday() < 3:
                    run_date = active[key][2] + datetime.timedelta(days=1)
                else:
                    run_date = active[key][2] + datetime.timedelta(days=3)
                run_date = run_date.replace(hour=7, minute=0, second=0)
                active[key][2] = run_date
        print('{}  |  {}  |  {}'.format(key, active[key][0], active[key][2].strftime(fmt)))
        #f.write('{}  |  {}  |  {}'.format(key, active[key][0], active[key][2].strftime(fmt)))
        
       
        #TODO:add write to file for current jobs

#function to calculate next available employee        
def whos_next():
    d = {}
    for key in active:
        d[key] = active[key][2]
    try:
        return min(d, key = d.get)
    except TypeError:
        pass
            

#assigns jobs in stack based on employee availability    
def job_assign():
    input('Starting job assignment, press enter to continue > ')
    schedule = []
    print('Job Number | Customer | Part Number | Scheduled Start | Scheduled Done | Employee')
    while stack:
        
        next_emp = whos_next()
        input('the next available employee is {}'.format(next_emp))
        start_time = active[next_emp][2]
        next_job = stack.pop(0)        
        routed_time = next_job[5]
        finish_time = count_forward(start_time, routed_time)       
        schedule.append([next_job[0], next_job[1], next_job[2], start_time, finish_time, next_emp ])
        active[next_emp][0] = next_job[0]
        active[next_emp][2] = finish_time
        print('{} | {} | {} | {} | {} | {}'.format(next_job[0], next_job[1], next_job[2], start_time, finish_time, next_emp))
        #print('updated active')
        print('_______________')
    
        
    sched_df = pandas.DataFrame(schedule)   
    sched_df.columns = ['Job Number', 'Customer', 'Part Number', 'Scheduled Start', 'Scheduled Done', 'Employee']
    sched_df.sort_values(by='Scheduled Start')
    print(sched_df)
    filedate = datetime.datetime.now().strftime('%m_%d_%y')
    print('Report Generated: {}'.format(filedate))
    sched_df.to_csv('finished_schedule.csv', sep=',', encoding='utf-8')
    

#find employee who will be done first
#pop first job from queue to active


currentjob()  
initialize()

#build priority stack

#List Index Helper:
#[0] = job number
#[1] = customer with space first
#[2] = partnum
#[3] = description
#[4] = due date
#[5] = routing
#[6] = prioritydate

         

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
pprint.pprint(job_routing)

#combine data to form raw unsorted queue
for list in orderdata:
    try:
        list.append(round(job_routing[list[0]],1))
    except KeyError:
        continue

#Assign priority date and alert if no routing
Prioritized = []
for list in orderdata:
    if len(list) == 6:
        if list[5] == None:
            notrouted.append(list[0])
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
stack_purge()
#pprint.pprint(stack)
df.to_csv('out.csv', encoding='utf-8')
print('The following jobs have no routing and will be ommitted from schedule: ')
pprint.pprint(notrouted)

job_assign()
