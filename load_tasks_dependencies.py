import numpy as np
import pandas as pd
import json
from datetime import datetime
from copy import deepcopy
import bisect
from collections import defaultdict
from itertools import cycle
from typing import Dict, Tuple
import matplotlib.pyplot as plt
import random

from utils import *
from config import *



def load_tasks_dependencies(path):
    '''
    Load objects tasks, task_count, task2childs, task2parents, functions task2childs and task2parents
    '''
    
    print("Loading task graph...")
    #Load task graph
    file = open(path)
    data = json.load(file)
    nodes = data['nodes']
    tasks = dict()
    for task_str, info in nodes.items():
        task = int(task_str)
        tasks[task] = {'Data' : string2duration(info['Data']), 'Dependencies' : info['Dependencies']}
    #Load task count
    task_count = len(tasks)
    print("Data loaded successfully. Number of tasks: " + str(task_count))
    
    #Load tasks to child tasks / Tasks to parents / Task is terminal / Task is inital
    task2childs = {task : list() for task in tasks}
    task2parents = {task : list() for task in tasks}
    for task, info in tasks.items():
        #Add childs
        list_task_parents = info['Dependencies']
        for task_parent in list_task_parents:
            task2childs[task_parent].append(task)
        #Add parents
        task2parents[task] = tasks[task]['Dependencies']
    
    def task_is_terminal(task: int):
        return len(task2childs[task]) == 0
    def task_is_inital(task: int):
        return len(task2parents[task]) == 0
    
    #Load the task2sbl dict
    print("Loading SBL...")
    def save_static_bottom_level(task : int, task2sbl):
        '''Compute sbl of task (by calling recursively save_sbl(child tasks) and save it in the dict tasks2sbl)
        '''
        task_duration = tasks[task]["Data"]
        if task_is_terminal(task):
            sbl = task_duration
        else:
            list_sbl_child = list()
            for task_child in task2childs[task]:
                if task_child in task2sbl:
                    sbl_child = task2sbl[task_child]
                else:
                    sbl_child = save_static_bottom_level(task_child, task2sbl)
                list_sbl_child.append(sbl_child)
            sbl = max(list_sbl_child) + task_duration
        task2sbl[task] = sbl
        return sbl
    
    task2sbl = dict()
    for task in tasks:
        if task_is_inital(task):
            save_static_bottom_level(task, task2sbl)
    print("Task data loaded.")
    return tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal

    
if __name__ == '__main__':
    load_tasks_dependencies(filename)