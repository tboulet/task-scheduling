
import json
from datetime import datetime
def n2letter(n):
    '''0 to 'a', 1 to 'b', ... '''
    return str(n)
    
def string2duration(string):
    ''' "01:50:19.3177493" to duration in seconds'''
    date =  datetime.strptime(string.split('.')[0], "%H:%M:%S")
    return date.second + 60*date.minute + 3600*date.hour


def read_data(path):
    file = open(path)
    data = json.load(file)
    nodes = data['nodes']
    tasks = dict()
    for task_str, info in nodes.items():
        task = int(task_str)
        tasks[task] = {'Data' : string2duration(info['Data']), 'Dependencies' : info['Dependencies']}
    task_count = len(tasks)
    print("Data loaded successfully. Number of tasks: " + str(task_count))
    return tasks, task_count


def load_dependencies(tasks):
    #Tasks to child tasks / Tasks to parents / Task is terminal / Task is inital
    task2childs = {task : list() for task in tasks}
    task2parents = {task : list() for task in tasks}
    for task, info in tasks.items():
        #Add childs
        list_task_parents = info['Dependencies']
        for task_parent in list_task_parents:
            task2childs[task_parent].append(task)
        #Add parents
        task2parents[task] = tasks[task]['Dependencies']
    
    return task2childs, task2parents
    
def task_is_terminal(task, task2childs):
    return len(task2childs[task]) == 0
def task_is_inital(task, task2parents):
    return len(task2parents[task]) == 0


def save_static_bottom_level(task, tasks, task2childs, task2sbl):
    task_duration = tasks[task]["Data"]
    if task_is_terminal(task, task2childs):
        sbl = task_duration
    else:
        list_sbl_child = list()
        for task_child in task2childs[task]:
            if task_child in task2sbl:
                sbl_child = task2sbl[task_child]
            else:
                sbl_child = save_static_bottom_level(task_child, tasks, task2childs, task2sbl)
            list_sbl_child.append(sbl_child)
        sbl = max(list_sbl_child) + task_duration
                
    task2sbl[task] = sbl
    return sbl

def sbl(tasks, task2childs, task2parents):
    task2sbl = {}
    for task in tasks:
        if task_is_inital(task, task2parents):
            save_static_bottom_level(task, tasks, task2childs, task2sbl)
    return task2sbl