import json
import datetime
from queue import PriorityQueue
import numpy as np
numCores = 2
def convert_time(time_str):
    times = time_str.split(':')
    return np.float32(times[0])*3600 + np.float32(times[1])*60 + np.float32(times[2])


def computeChilds(taskList, num_tasks):
    for i in range(num_tasks):
        for item in taskList[i][2]:
            taskList[item][3].append(i)
    return
    
def task_is_terminal(task: int):
    return len(taskList[task][3]) == 0
def task_is_inital(task: int):
    return len(taskList[task][2]) == 0

def read_data(path):
    global task_count
    file = open(path)
    global data
    data = json.load(file)
    task_count = len(data["nodes"])
    print("Data loaded successfully. Number of tasks: " + str(task_count))
    index = np.int32(1)
    list_nodes = []
    for node in data['nodes']:
        time = convert_time(data['nodes'][str(index)]['Data'])
        dependencies = []
        for d in data['nodes'][str(index)]['Dependencies']:
            dependencies.append(np.int32(d))
        list_nodes.append((index, time, dependencies, [])) 
        index +=1
    return list_nodes, task_count

def IDA_star():
    initial = 
    pass

class Node():
    def __init__(self, parent=None, task=None, core=None):
        if parent is None:
            

taskList, numTasks = read_data("./smallRandom.json")

task2childs = [[] for i in range(numTasks)]
task2parents = [[] for i in range(numTasks)]
computeChilds(taskList, numTasks)


print(taskList)