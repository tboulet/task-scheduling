from collections import defaultdict

from matplotlib import pyplot as plt
import pandas as pd


def cycle(lst: list[str]):
    x = lst.pop(0)
    lst.append(x)
    return x

def plot_schedule(node, critical_path=[]):
    schedule = node.schedule
    colors_by_proc = defaultdict(lambda:
        ['tab:blue', 'tab:orange', 'tab:green', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'])
    for id, (start, end, proc) in schedule.items():
        # cycle through the colors for this processor
        color = cycle(colors_by_proc[proc])
        colors_by_proc[proc].append(color)
        
        # handle critical path nodes
        if id in critical_path:
            critical_kwargs = {
                'edgecolor': 'red',
                'lw': 2,
                'zorder': 100,
            }
        else:
            critical_kwargs = {}
        
        # blot the bar and text
        plt.broken_barh([(start, end-start)],
                        (proc-.4, .8),
                        facecolors=color,
                        **critical_kwargs)
        #plt.annotate(str(id),
        #                xy=((start+end)/2, proc),
        #                ha='center',
        #                va='center',
        #                zorder=101)
    plt.yticks(list(colors_by_proc.keys()), [f'Proc {proc}' for proc in colors_by_proc.keys()])
    plt.tight_layout()
    plt.show()