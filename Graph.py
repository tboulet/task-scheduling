from utils import *
from Node import Node
class Graph:
    def __init__(self, path, n_cores = 2, alpha = 1):
        self.tasks, self.task_count = read_data(path) 
        self.tasks_to_child, self.tasks_to_parent = load_dependencies(self.tasks)
        self.tasks_to_sbl = sbl(self.tasks, self.tasks_to_child, self.tasks_to_parent)
        self.n_cores = n_cores
        self.alpha = alpha
        self.root = Node(n_cores)
    
    def equal(self, node1, node2):
        '''Return whether a node is equal to another. Two nodes are considered equal if they have completed the same tasks and if all their cores stop working at same time.
        '''
        if node1.g != node2.g:
            return False       
        if node1.tasks_done_time != node2.tasks_done_time:
            return False
        return node1.set_of_core() == node2.set_of_core()

    def cost(self, current, next):
        '''Return the cost of going from self to child_node, a child node of self
        '''
        res = next.g - current.g
        if res < 0:
            raise Exception("Cost difference is negative")
        return res
    
    def is_solved(self, node):
        '''Return whether a node is a full schedule'''
        return len(node.tasks_done_time) == self.task_count
    
    def h(self, node):
        '''Estimated remaining time of the node-schedule for reaching a terminal node. Must understimate true value.
        '''
        successor_tasks = list()
        for task, info in self.tasks.items():
            if task in node.tasks_done_time: #On passe les taches déjà ajoutées
                continue    #O(n_task)
            
            pass_task = False #On passe les tâches auquels il manque au moins une dépendance dans tasks_done
            for task_required in info['Dependencies']:
                if task_required not in node.tasks_done_time:
                    pass_task = True
                    break
            if pass_task:
                continue
            
            successor_tasks.append(task)
        if len(successor_tasks) == 0:
            return 0
        return self.alpha*max([self.tasks_to_sbl[task] for task in successor_tasks])
    
    def n_successors(self, node):
        return len(self.successors(node))
    
    def successor(self, node, i):
        return sorted(self.successors(node), key = lambda n: n.g + self.h(n))[i]
    
    def successors(self, node):
        childs = list()
        #On regarde toutes les tâches qu'on va tenter de rajouter
        for task, info in self.tasks.items():
            
            #On passe les taches déjà ajoutées
            if task in node.tasks_done_time: 
                continue
            
            #On ne garde que les taches dont toutes les dépendances ont été réalisées
            if not all([task_required in node.tasks_done_time for task_required in info['Dependencies']]): 
                continue
            
            #On calcul le temps ou toutes les dépendances de task seront terminés par les coeurs   
            time_all_tasks_done = max([0] + [node.tasks_done_time[task_required] for task_required in info['Dependencies']])
                                         
            for core_n, core in node.cores.items():
                #On ne commence à faire la task que lorsque toutes les dépendances sont calculées et que le core est disponible.
                time_core_available = core["task_end_time"]
                time_task_start = max(time_all_tasks_done, time_core_available)
                task_end_time = time_task_start + self.tasks[task]['Data']
                child = Node(n_cores = self.n_cores, parent = node, task_to_add=task, core_where_to_add=core_n, time_task_start=time_task_start, task_end_time=task_end_time)    
                childs.append(child)
                
        return childs