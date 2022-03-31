import time
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

from torch import take_along_dim

from utils import *
from visualisation import plot_schedule

from config import n_cores, filename, alpha
from load_tasks_dependencies import load_tasks_dependencies
from task_graph_generator import generate_task_graph
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
    
    start = time.perf_counter()
    final_node = ida_star(Node(graph=graph))
    dt = time.perf_counter() - start
    
    score = final_node.f
    error_ratio = (score - critical_path_score)/critical_path_score
    return dt, error_ratio, score, final_node
    
    
    
    
if __name__ == '__main__':
    nodes = generate_task_graph(10, 2.0, 1000.0, 500.0, "graph.json")
    tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal = load_tasks_dependencies(path = filename)
    tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal = load_tasks_dependencies(nodes = nodes)
    dt, error_ratio, score, final_node = run(tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal, n_cores=n_cores, alpha=alpha)
    
    print("Temps de calcul en seconde:", dt)
    print("Error ratio:", error_ratio)
    print("Score:", score)
    plot_schedule(final_node)