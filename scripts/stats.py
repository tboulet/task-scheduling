#Statistics about influence of parameters on time complexity and performance of the algorithm.

import sys
import time

from matplotlib import pyplot as plt
from tqdm import tqdm
from utils import *
from config import *
from visualization import plot_schedule
from task_generator import generate_task_graph, fileToGraph, plot_graph
from graph import Graph
from ida import ida_star, verify, random_choice

def run(filename, recul = 1, n_cores = 2, alpha = 1, beta = 8):
    '''Run an IDA star algorithm on the graph given and with corresponding cores and alpha parameters.
    Return metrics.
    '''
    graph = Graph(filename, n_cores, alpha)
    perfect_score = graph.best_time()
    
    start = time.perf_counter()
    final_node = ida_star(graph, recul, perfect_score*beta)
    dt = time.perf_counter() - start
    
    error_ratio, score = verify(graph, final_node)
    random_ratio, random_score = 0, 0
    for _ in range(K := 10):
        random_final_node = random_choice(graph)
        random_ratio_i, random_score_i = verify(graph, random_final_node)
        random_ratio += random_ratio_i / K
        random_score += random_score_i / K
    return dt, error_ratio, random_ratio, score, random_score, final_node
    
if __name__ == '__main__':
    # plt.ylim(bottom = 0)
    
    #ONE RUN
    if False:
        dt, ratio, random_ratio, score, random_score, final_node = run(filename, recul=recul, n_cores=n_cores, alpha=alpha)
        print("Temps de calcul en seconde:", dt)
        print("Error ratio:", ratio)
        print("Error ratio random:", random_ratio)
        print("Score:", score)
        print("Score random:", random_score)
        G = fileToGraph(filename) 
        plot_graph(G)
        plt.show()
        plt.figure()
        plot_schedule(final_node)
        plt.show()
        sys.exit()



    print(f"Searching a solution for : {filename}")
    
    if False:
        #N_CORE
        nodes = generate_task_graph(100, 5.0, 1000.0, 500.0, "graph.json")
        L_cores = [c for c in range(1, 10)]
        L_times = list()
        L_ratios = list()
        L_ratios_random = list()
        for n_core in  tqdm(L_cores):
            dt, ratio, random_ratio, score, random_score, final_node = run(filename, n_cores=n_core, alpha=1, recul=1, beta = 8)
            L_times.append(dt)
            L_ratios.append(ratio)
            L_ratios_random.append(random_ratio)
        norm = max(L_ratios_random)/L_times[-1]
        L_times = [t*norm for t in L_times]
        plt.plot(L_cores, L_times, 'g-', label = "Execution time (normalized)")
        plt.plot(L_cores, L_ratios, 'r-', label = "Score/critical_path_score ratio")
        plt.plot(L_cores, L_ratios_random, 'b-', label = "Random Score/critical_path_score ratio")
        plt.xlabel("n_cores = number of cores")
        plt.legend()
        plt.show()
        sys.exit()
        
    if False:
        #N_TASK
        L_task = [n for n in range(5, 160, 5)]
        L_times = list()
        L_ratios = list()
        L_ratios_random = list()
        for n_task in  tqdm(L_task):
            nodes = generate_task_graph(n_task, 5.0, 1000.0, 500.0, "graph.json")
            dt, ratio, random_ratio, score, random_score, final_node = run(filename, n_cores=8, alpha=1, recul=1, beta = 8)
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
        sys.exit()
        
    
    if True:
        #N_DEP
        L_dep = [n for n in range(1, 20)]
        L_times = list()
        L_ratios = list()
        L_ratios_random = list()
        for n_dep in  tqdm(L_dep):
            nodes = generate_task_graph(100, n_dep, 1000.0, 500.0, "graph.json")
            dt, ratio, random_ratio, score, random_score, final_node = run(filename, n_cores=8, alpha=1, recul=1, beta = 10)
            L_times.append(dt)
            L_ratios.append(ratio)
            L_ratios_random.append(random_ratio)
        L_times = [t/L_times[-1] for t in L_times]
        plt.plot(L_dep, L_times, 'g-', label = "Execution time (normalized)")
        plt.plot(L_dep, L_ratios, 'r-', label = "Score/critical_path_score ratio")
        plt.plot(L_dep, L_ratios_random, 'b-', label = "Random Score/critical_path_score ratio")
        plt.xlabel("n_dep = mean number of dependencies")
        plt.legend()
        plt.show()
        sys.exit()


    if True:
        #N_BETA 
        nodes = generate_task_graph(30, 3, 1000.0, 500.0, "graph.json")
        L_beta = [n for n in range(2, 40)]
        L_times = list()
        L_ratios = list()
        L_ratios_random = list()
        for beta in  tqdm(L_beta):
            
            dt, ratio, random_ratio, score, random_score, final_node = run(filename, n_cores=2, alpha=1, recul=1, beta = beta)
            L_times.append(dt)
            L_ratios.append(ratio)
            L_ratios_random.append(random_ratio)
        L_times = [t/L_times[-1] for t in L_times]
        plt.plot(L_beta, L_times, 'g-', label = "Execution time (normalized)")
        plt.plot(L_beta, L_ratios, 'r-', label = "Score/critical_path_score ratio")
        plt.plot(L_beta, L_ratios_random, 'b-', label = "Random Score/critical_path_score ratio")
        plt.xlabel("beta")
        plt.legend()
        plt.show()