import numpy as np
from node import Node
import pandas as pd
from random import randint

def random_choice(graph):
    '''Return a random total scheduling from a graph.
    '''
    node = graph.root
    while not graph.is_solved(node):
        index = randint(0, graph.n_successors(node) - 1)
        node = graph.successor(node, index)
    return node

def step_back(graph, node, bound, depth, fast):
    stack = [node]
    indexes = [0]
    minimum = np.inf
    best = node
    while (len(stack)):
        current = stack[-1]
        index = indexes[-1]

        if fast:
            f = current.g + graph.h(current)
        else:
            f = current.g

        if len(stack) == depth:
            if f < minimum:
                minimum = f
                best = current
        
        if f > bound:
            stack.pop()
            indexes.pop()
            continue

        if graph.is_solved(current):
            if current.g < minimum:
                minimum = current.g
                best = current

        if index >= graph.n_successors(current):
            stack.pop()
            indexes.pop()
            continue
        
        succ = graph.successor(current, index, fast)
        indexes[-1] = index + 1
        stack.append(succ)
        indexes.append(0)
    
    return best

def search(graph, stack, bound, recul, depth, fast):
    indexes = [0]
    while (len(stack)):
        node = stack[-1]
        index = indexes[-1]
        if fast:
            f = node.g
        else:
            f = node.g + graph.h(node)

        if f > bound:
            stack.pop()
            indexes.pop()
            continue

        if graph.is_solved(node):
            return step_back(graph, stack[-recul], bound, depth, fast)
        
        if len(stack) == depth:
            return node

        if index >= graph.n_successors(node):
            stack.pop()
            indexes.pop()
            continue
        
        succ = graph.successor(node, index, fast)
        indexes[-1] = index + 1
        stack.append(succ)
        indexes.append(0)
    
    return False

def ida_star(graph, recul = 1, limit = np.inf, depth = np.inf, fast = True):
    bound = limit*graph.alpha
    stack = [graph.root]
    t = search(graph, stack, bound, recul + 1, depth, fast)
    if isinstance(t, Node):
        return t
    return None

def verify(graph, node):
    solution_df = pd.DataFrame.from_dict(node.schedule, orient='index', columns=['start', 'end', 'core'])
    score = solution_df['end'].max()
    bestscore = graph.best_time()
    if  bestscore > score:
        return False

    for task in solution_df.index:
        for parent in graph.tasks[task]['Dependencies']:
            if solution_df.loc[parent]['end'] > solution_df.loc[task]['start']:
                return False
    print(score, bestscore)
    return (100*(score - bestscore)/bestscore)
