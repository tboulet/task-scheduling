from random import randint
import numpy as np
from node import Node
import pandas as pd

def search(graph, stack, bound, recul, depth):
    '''Search function for the IDA* algorithm. 
    '''
    indexes = [0]
    while (len(stack)):
        node = stack[-1]
        index = indexes[-1]

        f = node.g + graph.h(node)

        #Don't explore the branch if its f_score estimated excess a fixed bound value.
        if f > bound:
            stack.pop()
            indexes.pop()
            continue

        if graph.is_solved(node):
            return min(graph.successors(stack[-recul]), key=lambda n: n.g + graph.h(n))
        
        if len(stack) == depth:
            return min(graph.successors(stack[-recul]), key=lambda n: n.g + graph.h(n))

        if index >= graph.n_successors(node):
            stack.pop()
            indexes.pop()
            continue
        
        succ = graph.successor(node, index)
        indexes[-1] = index + 1
        stack.append(succ)
        indexes.append(0)
    
    #No path to the goal node were found
    return False

def ida_star(graph, recul = 1, limit = np.inf, depth = np.inf):
    bound = limit
    stack = [graph.root]
    t = search(graph, stack, bound, recul + 1, depth)
    if isinstance(t, Node):
        return t
    return None

def compute_best_time(graph):
    task_df = pd.DataFrame.from_dict(graph.tasks_to_sbl, orient='index', columns=['sbl'])
    best_time = task_df['sbl'].max()
    return best_time

def verify(graph, node):
    solution_df = pd.DataFrame.from_dict(node.schedule, orient='index', columns=['start', 'end', 'core'])
    score = solution_df['end'].max()
    best_time = compute_best_time(graph)
    if  best_time > score:
        return False

    for task in solution_df.index:
        for parent in graph.tasks[task]['Dependencies']:
            if solution_df.loc[parent]['end'] > solution_df.loc[task]['start']:
                return False
    return score/best_time, score



def random_choice(graph):
    '''Return a random total scheduling from a graph.
    '''
    node = graph.root
    while not graph.is_solved(node):
        index = randint(0, graph.n_successors(node) - 1)
        node = graph.successor(node, index)
    return node