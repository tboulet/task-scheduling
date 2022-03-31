import time

from matplotlib import pyplot as plt
from tqdm import tqdm
from load_tasks_dependencies import load_tasks_dependencies
from utils import *
from config import *
from visualization import plot_schedule
from task_generator import generate_task_graph
from graph import Graph
from ida import ida_star, compute_best_time, verify

def run(filename, recul = 1, n_cores = 2, alpha = 1):
    '''Run an IDA star algorithm on the graph given and with corresponding cores and alpha parameters.
    Return the time of execution, the error_ratio and the score.
    '''
    graph = Graph(filename, n_cores, alpha)
    perfect_score = compute_best_time(graph)
    
    start = time.perf_counter()
    final_node = ida_star(graph, recul, perfect_score*2)
    dt = time.perf_counter() - start
    
    error_ratio, score = verify(graph, final_node)
    return dt, error_ratio, score, final_node
    
if __name__ == '__main__':
    nodes = generate_task_graph(20, 2.0, 1000.0, 500.0, "graph.json")
    filename_graph = "graph.json"
    tasks, task_count, task2childs, task2parents, task2sbl, task_is_inital, task_is_terminal = load_tasks_dependencies(path = filename_graph)
    
    # dt, error_ratio, score, final_node = run(filename, recul=recul, n_cores=n_cores, alpha=alpha)
    # print("Temps de calcul en seconde:", dt)
    # print("Error ratio:", error_ratio)
    # print("Score:", score)
    # plot_schedule(final_node)

    #RATIO = f(n_core)
    L_c = [c for c in range(2, 10)]
    L_t = list()
    L_r = list()
    for n_core in  tqdm(L_c):
        filename = "graph.json"
        dt, ratio, score, final_node = run(filename, n_cores=n_core, alpha=1, recul=1)
        L_t.append(dt)
        L_r.append(ratio)
    L_t = [t/L_t[-1] for t in L_t]
    plt.plot(L_c, L_t, 'g-', label = "Execution time (normalized)")
    plt.plot(L_c, L_r, 'r-', label = "Score/critical_path_score ratio")
    plt.legend()
    plt.show()
    plot_schedule(final_node)