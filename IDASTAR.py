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

from NODE import Node

def search_goal(path, g, bound, goal):
    node = path[-1]
    f = g + node.h()
    if f > bound:
        return f
    if node == goal:
        return node
    minimum = np.inf
    for succ in node.successors():
        if succ not in path:
            path.append(succ)
            t = search_goal(path, g + node.cost(succ), bound, goal)
            if isinstance(t, Node):
                return t
            elif t < minimum:
                minimum = t
            path.pop()
    return minimum

def search_solved(path, g, bound):
    node = path[-1]
    f = g + node.h()
    if f > bound:
        return f
    if node.is_solved():
        best_node = sorted(path[-2].successors(), key = lambda n : n.g)[0]
        path[-1] = best_node
        return best_node
    minimum = np.inf
    for succ in node.successors():
        if succ not in path:
            path.append(succ)
            t = search_solved(path, g + node.cost(succ), bound)
            if isinstance(t, Node):
                return t
            elif t < minimum:
                minimum = t
            path.pop()
    return minimum


def ida_star(root, goal = None):
    bound = root.h()*2
    path = [root]
    if goal:
        t = search_goal(path, 0, bound, goal)
    else:
        t = search_solved(path, 0, bound)
    if isinstance(t, Node):
        return t
    return 'Not found'