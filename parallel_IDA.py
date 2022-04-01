
import task_graph_generator
from Graph import Graph
from Node import Node
import numpy as np
from utils import *
from mpi4py import MPI



def search(stack, bound, depth):
    indexes = [0]
    while (len(stack)):
        node = stack[-1]
        index = indexes[-1]

        f = node.g + graph.h(node)

        if graph.is_solved(node):
            return sorted(graph.successors(stack[-2]), key=lambda n: n.g)[0]
        
        if len(stack) == depth:
            return sorted(graph.successors(stack[-2]), key=lambda n: n.g + graph.h(n))

        if f > bound:
            stack.pop()
            indexes.pop()
            continue

        if index >= graph.n_successors(node):
            stack.pop()
            indexes.pop()
            continue
        
        succ = graph.successor(node, index)
        indexes[-1] = index + 1
        stack.append(succ)
        indexes.append(0)
    
    return False


def ida_star(depth = np.inf):
    bound = graph.h(graph.root)*2
    stack = [graph.root]
    t = search(stack, bound, depth)
    if isinstance(t, Node):
        print('Done')
        return t
    print('Not found')
    return None


def main():
    global graph
    best_nodes = []
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        graph = Graph('../Graphs/xsmallComplex.json', 6, 1)
        depth = 5
        bound = graph.h(graph.root)*2
        stack = [graph.root]
        branches = search(stack, bound, depth)[:size]
        for i in range(i):
            comm.bsend(branches, i)
        while True:
            comm.recv(best_nodes)
    else:
        node = None
        comm.recv(node, 0)
        print(node)
    pass

if __name__ == "__main__":
    main()