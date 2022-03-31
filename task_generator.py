import networkx as nx
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

    nodes = {str(i+1) : {} for i in G.nodes()}
    for id, value in nodes.items():
        value["Data"] =  float_to_time(max(np.random.normal(time_mean, time_desviation),time_mean/10))
        value["Dependencies"] = []
    for u,v in DAG.edges():
        nodes[str(v+1)]["Dependencies"].append(u+1)

    if path_to_save != None:
        file = open(path_to_save, "w")
        json.dump({"nodes" : nodes}, file, indent=4)
    print(nodes)
    return nodes


def main():
    nodes = generate_task_graph(10, 2.0, 1000.0, 500.0, "graph.json")
    print(nodes)
    pass

if __name__ == "__main__":
    main()