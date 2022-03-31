import networkx as nx
#import matplotlib.pyplot as plt
import numpy as np
import json


def float_to_time(time : float):
    hours = int(time // 3600)
    time = time - hours*3600
    minutes = int(time // 60)
    time = time - minutes*60
    seconds = int(time // 1)
    time = int((time - seconds)*10e6)
    return "{hours:02d}:{minutes:02d}:{seconds:02d}.{miliseconds:07d}".format(hours = hours, minutes = minutes, seconds = seconds, miliseconds = time)


def generate_task_graph(number_tasks : int, dependencies_mean : float, time_mean : float, time_desviation : float, path_to_save : str):
    G=nx.fast_gnp_random_graph(number_tasks,dependencies_mean/number_tasks,directed=True)
    DAG = nx.DiGraph()
    DAG.add_nodes_from(range(0,number_tasks))
    DAG.add_edges_from([(u,v) for (u,v) in G.edges() if u<v])
    
    
    #nx.draw(DAG)
    #plt.show() #TO VISUALIZE THE GRAPH

    nodes = {i+1 : {} for i in G.nodes()}
    for id, value in nodes.items():
        value["Data"] =  float_to_time(max(np.random.normal(time_mean, time_desviation),0))
        value["Dependencies"] = []
    for u,v in DAG.edges():
        nodes[v]["Dependencies"].append(u)

    if path_to_save != None:
        file = open(path_to_save, "w")
        json.dump({"nodes" : nodes}, file, indent=4)
    return nodes


def main():
    #nodes = generate_task_graph(10, 2.0, 1000.0, 500.0, "graph.json")
    pass

if __name__ == "__main__":
    main()