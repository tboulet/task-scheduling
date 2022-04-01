import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches
import numpy as np
import json




def save_static_bottom_level(node, G, sbl):
    w = 1
    if G.out_degree(node) == 0:
        sbl[node] = 0
        return sbl[node]
    else:
        childs = list()
        for source, child in G.out_edges(node):
            if child in sbl:
                sbl_child = sbl[child]
            else:
                sbl_child = save_static_bottom_level(child, G, sbl)
            childs.append(sbl_child)
        sbl_calculated = max(childs) + w
                
    sbl[node] = sbl_calculated
    return sbl[node]

def bottom_level(G):
    sbl = {}
    for node in G.nodes():
        if not G.in_edges(node):
            save_static_bottom_level(node, G, sbl)
    return sbl

def float_to_time(time : float):
    hours = int(time // 3600)
    time = time - hours*3600
    minutes = int(time // 60)
    time = time - minutes*60
    seconds = int(time // 1)
    time = int((time - seconds)*10e6)
    return "{hours:02d}:{minutes:02d}:{seconds:02d}.{miliseconds:07d}".format(hours = hours, minutes = minutes, seconds = seconds, miliseconds = time)

def read_data(path):
    file = open(path)
    data = json.load(file)
    nodes = data['nodes']
    tasks = dict()
    for task_str, info in nodes.items():
        task = int(task_str)
        tasks[task] = {'Dependencies' : info['Dependencies']}
    task_count = len(tasks)
    print("Data loaded successfully. Number of tasks: " + str(task_count))
    return tasks, task_count


def fileToGraph(path):
    graph, count = read_data(path)
    G = nx.DiGraph()
    G.add_nodes_from(graph)
    for node in graph:
        for edge in graph[node]["Dependencies"]:
            G.add_edge(edge, node)
    G = nx.convert_node_labels_to_integers(G, 0)
    return G

def plot_graph(G):
    sbl = bottom_level(G)
    max_sbl = max(sbl.values())
    pos = {}
    shift = np.zeros(max_sbl+1)
    for node in G.nodes():
        pos[node+1] = (max_sbl-sbl[node],shift[max_sbl-sbl[node]])
        shift[max_sbl-sbl[node]] +=1

    plt.figure(figsize=(15,5))
    G = nx.convert_node_labels_to_integers(G, 1)
    ax = plt.gca()

    for edge in G.edges():
        target, source = edge
        rad = 0.1
        rad = rad if source%2 else -rad
        ax.annotate("",
                    xy=pos[source],
                    xytext=pos[target],
                    arrowprops=dict(arrowstyle=matplotlib.patches.ArrowStyle("->", head_length=1, head_width=1),color="black",
                                    connectionstyle="arc3,rad="+str(rad),
                                    alpha=0.6,
                                    linewidth=1.5))

    nx.draw_networkx_nodes(G, pos=pos, node_size=500, node_color='black')
    nx.draw_networkx_labels(G, pos=pos, font_color='white')
    plt.box(False)
    plt.show()

def generate_task_graph(number_tasks : int, dependencies_mean : float, time_mean : float, time_desviation : float, path_to_save : str):
    G=nx.fast_gnp_random_graph(number_tasks,dependencies_mean/number_tasks,directed=True)
    DAG = nx.DiGraph()
    DAG.add_nodes_from(range(0,number_tasks))
    DAG.add_edges_from([(u,v) for (u,v) in G.edges() if u<v])
    
    nodes = {str(i+1) : {} for i in DAG.nodes()}
    for id, value in nodes.items():
        value["Data"] =  float_to_time(max(np.random.normal(time_mean, time_desviation),time_mean/10))
        value["Dependencies"] = []
    for u,v in DAG.edges():
        nodes[str(v+1)]["Dependencies"].append(u+1)

    if path_to_save != None:
        file = open(path_to_save, "w")
        json.dump({"nodes" : nodes}, file, indent=4)

    # TO PLOT THE GRAPH
    plot_graph(DAG)
    
    return nodes


def main():
    #nodes = generate_task_graph(100, 2.0, 1000.0, 500.0, "graph.json") #GENERATE RANDOM
    #print(nodes)

    #G = fileToGraph("../Graphs/graph.json") GENERATE G FROM A FILE
    #plot_graph(G)
    pass

if __name__ == "__main__":
    main()