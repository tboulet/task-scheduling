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
from visualisation import plot_schedule

from config import n_cores, filename, alpha
from load_tasks_dependencies import load_tasks_dependencies
from NODE import Node
from IDASTAR import ida_star

    
def run(tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal, 
        n_cores = 2, alpha = 1):
    '''Run an IDA star algorithm on the graph given and with corresponding cores and alpha parameters.
    Return the time of execution, the error_ratio and the score.
    '''
    critical_path_score = max([task2sbl[task] for task in tasks if task_is_inital(task)])
    
    class Graph:
        def __init__(self):
            self.tasks = tasks
            self.tasks_to_sbl = task2sbl
            self.tasks_to_parent = task2parents
            self.tasks_to_child = task2childs
            self.n_cores = n_cores
            self.alpha = alpha
            self.task_count = task_count
    graph = Graph()
        
    final_node = ida_star(Node(graph=graph))
    
    score = final_node.f
    error_ratio = (score - critical_path_score)/critical_path_score
    return 0, error_ratio, score, final_node
    
    
    
    
if __name__ == '__main__':
    tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal = load_tasks_dependencies(filename)
    dt, error_ratio, score, final_node = run(tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal, n_cores=n_cores, alpha=alpha)
    print(dt)
    print(error_ratio)
    print(score)
    plot_schedule(final_node)