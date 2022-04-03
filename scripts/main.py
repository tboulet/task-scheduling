from isort import file
from matplotlib import pyplot as plt
from config import filename, n_cores, alpha, recul, beta
from ida import ida_star
from visualization import plot_schedule
from graph import Graph

if __name__ == '__main__':
    print(f"Search a solution for {filename}...")
    graph = Graph(path = filename, n_cores=n_cores, alpha=alpha)
    perfect_score = graph.best_time()
    final_node = ida_star(graph, recul, perfect_score*beta, filename = filename)
    plot_schedule(final_node)
    plt.show()
    print(f"Result saved in {filename[:-5]}_schedule.json")