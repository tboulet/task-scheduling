import time
from utils import *
from config import *
from visualization import plot_schedule
from task_generator import generate_task_graph
from graph import Graph
from ida import ida_star, best_time, verify

def run(filename, recul = 1, n_cores = 2, alpha = 1):
    '''Run an IDA star algorithm on the graph given and with corresponding cores and alpha parameters.
    Return the time of execution, the error_ratio and the score.
    '''
    graph = Graph(filename, n_cores, alpha)
    perfect_score = best_time(graph)
    
    start = time.perf_counter()
    final_node = ida_star(graph, recul, perfect_score*2)
    dt = time.perf_counter() - start
    
    error_ratio, score = verify(graph)
    return dt, error_ratio, score, final_node
    
if __name__ == '__main__':
    nodes = generate_task_graph(10, 2.0, 1000.0, 500.0, "graph.json")
    dt, error_ratio, score, final_node = run(filename, recul=recul, n_cores=n_cores, alpha=alpha)
    
    print("Temps de calcul en seconde:", dt)
    print("Error ratio:", error_ratio)
    print("Score:", score)
    plot_schedule(final_node)