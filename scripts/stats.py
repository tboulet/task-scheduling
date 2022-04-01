import time

from matplotlib import pyplot as plt
from tqdm import tqdm
from load_tasks_dependencies import load_tasks_dependencies
from utils import *
from config import *
from visualization import plot_schedule
from task_generator import generate_task_graph
from graph import Graph
from ida import ida_star, compute_best_time, verify, random_choice

def run(filename, recul = 1, n_cores = 2, alpha = 1):
    '''Run an IDA star algorithm on the graph given and with corresponding cores and alpha parameters.
    Return the time of execution, the error_ratio and the score.
    '''
    graph = Graph(filename, n_cores, alpha)
    perfect_score = compute_best_time(graph)
    random_final_node = random_choice(graph)
    
    start = time.perf_counter()
    final_node = ida_star(graph, recul, perfect_score*2)
    dt = time.perf_counter() - start
    
    error_ratio, score = verify(graph, final_node)
    random_ratio, random_score = verify(graph, random_final_node)
    return dt, error_ratio, random_ratio, score, random_score, final_node
    
if __name__ == '__main__':
    nodes = generate_task_graph(20, 2.0, 1000.0, 500.0, "graph.json")
    print("Nodes generated.")
    
    #ONE RUN
    if False:
        dt, ratio, random_ratio, score, random_score, final_node = run(filename, recul=recul, n_cores=n_cores, alpha=alpha)
        print("Temps de calcul en seconde:", dt)
        print("Error ratio:", ratio)
        print("Error ratio random:", random_ratio)
        print("Score:", score)
        print("Score random:", random_score)
        plot_schedule(final_node)




    print(f"Searching a solution for : {filename}")
    
    if True:
        #RATIO, RATIO_RANDOM, TPS_EXEC = f(n_core)
        L_cores = [c for c in range(2, 20)]
        L_times = list()
        L_ratios = list()
        L_ratios_random = list()
        for n_core in  tqdm(L_cores):
            dt, ratio, random_ratio, score, random_score, final_node = run(filename, n_cores=n_core, alpha=1, recul=1)
            L_times.append(dt)
            L_ratios.append(ratio)
            L_ratios_random.append(random_ratio)
        L_times = [t/L_times[-1] for t in L_times]
        plt.plot(L_cores, L_times, 'g-', label = "Execution time (normalized)")
        plt.plot(L_cores, L_ratios, 'r-', label = "Score/critical_path_score ratio")
        plt.plot(L_cores, L_ratios_random, 'b-', label = "Random Score/critical_path_score ratio")
        plt.xlabel("n_cores = number of cores")
        plt.legend()
        plt.show()
        raise
        
    if False:
        #RATIO, RATIO_RANDOM, TPS_EXEC = f(n_task)
        L_task = [n for n in range(5, 50, 5)]
        L_times = list()
        L_ratios = list()
        L_ratios_random = list()
        for n_task in  tqdm(L_task):
            nodes = generate_task_graph(n_task, 3.0, 1000.0, 500.0, "graph.json")
            dt, ratio, random_ratio, score, random_score, final_node = run(filename, n_cores=4, alpha=1, recul=1)
            L_times.append(dt)
            L_ratios.append(ratio)
            L_ratios_random.append(random_ratio)
        L_times = [t/L_times[-1] for t in L_times]
        plt.plot(L_task, L_times, 'g-', label = "Execution time (normalized)")
        plt.plot(L_task, L_ratios, 'r-', label = "Score/critical_path_score ratio")
        plt.plot(L_task, L_ratios_random, 'b-', label = "Random Score/critical_path_score ratio")
        plt.xlabel("n_tasks = number of tasks")
        plt.legend()
        plt.show()
        
    
    if True:
        #RATIO, RATIO_RANDOM, TPS_EXEC = f(n_dep)
        L_task = [n for n in range(1, 20)]
        L_times = list()
        L_ratios = list()
        L_ratios_random = list()
        for n_dep in  tqdm(L_task):
            nodes = generate_task_graph(24, n_dep, 1000.0, 500.0, "graph.json")
            dt, ratio, random_ratio, score, random_score, final_node = run(filename, n_cores=4, alpha=1, recul=1)
            L_times.append(dt)
            L_ratios.append(ratio)
            L_ratios_random.append(random_ratio)
        L_times = [t/L_times[-1] for t in L_times]
        plt.plot(L_task, L_times, 'g-', label = "Execution time (normalized)")
        plt.plot(L_task, L_ratios, 'r-', label = "Score/critical_path_score ratio")
        plt.plot(L_task, L_ratios_random, 'b-', label = "Random Score/critical_path_score ratio")
        plt.xlabel("n_tasks = number of tasks")
        plt.legend()
        plt.show()