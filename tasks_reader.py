import json
from datetime import datetime
from math import inf


class Task():
    def __init__(self, id, duration, parents, childs):
        self.id = id
        self.duration = duration
        self.childs = childs
        self.parents = parents
        self.sbl = inf
        return
    def __repr__(self):
        return "{id: "+str(self.id)+", duration: "+str(self.duration)+", childs: "+str(self.childs)+", parents: "+str(self.parents)+"sbl: "+str(self.sbl)+"}"

def read_data(path):
    file = open(path)
    data = json.load(file)
    tasks_file = data['nodes']
    tasks = {}
    for task in tasks_file.keys():
        tasks[int(task)] = (Task(int(task), string2duration(tasks_file[task]['Data']), [int(i) for i in tasks_file[task]['Dependencies']], []))
    task_count = len(tasks)
    add_parents(tasks)
    return tasks

def add_parents(tasks):
    for task in tasks:
        for j in tasks[task].parents:
            tasks[j].childs.append(tasks[task].id)
    return tasks

def string2duration(string):
    ''' "01:50:19.3177493" to duration in seconds'''
    date =  datetime.strptime(string.split('.')[0], "%H:%M:%S")
    return date.second + 60*date.minute + 3600*date.hour

