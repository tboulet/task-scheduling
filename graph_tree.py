


from utils import n2letter


class Node():
    
    def __init__(self, graph, n_cores, task_count, parent = None, task_to_add = None, core_where_to_add = None, time_task_start = None):
        '''Create a Node object ie a partial scheduling
        parent = parent Node, None if root
        task_to_add : task added to the partial schedule
        core_where_to_add : core where to do task
        time_task_start : instant where the core will start computing the task
        '''
        self.task_count = task_count
        self.parent = parent
        
        if parent is None:
            self.graph = graph
            self.tasks_done_time = dict()
            self.cores = {core_n : {"task" : -1, "task_end_time" : 0} for core_n in range(n_cores)}
            
            self.g = 0
            self.f = self.h()
                   
            self.hist = ''  
            self.schedule = dict()
            
        else:
            if graph:
                self.graph = graph
            else:
                self.graph = self.parent.graph
            task_end_time = time_task_start + self.graph.tasks[task_to_add]['Data']
            self.tasks_done_time = parent.tasks_done_time.copy()
            self.tasks_done_time[task_to_add] = task_end_time

            self.cores = parent.cores.copy()
            self.cores[core_where_to_add] = {"task" : task_to_add, "task_end_time" : task_end_time}
                
            self.g = max(parent.g, task_end_time)
            self.f = max(self.g + self.h(), parent.f)
            #self.f = self.g + self.h()
            
            self.schedule = parent.schedule.copy()
            self.schedule[task_to_add] = (time_task_start, task_end_time, core_where_to_add)
            self.hist = parent.hist + f"|Task {task_to_add} start at time {time_task_start} on core {core_where_to_add} "
                 
    def __repr__(self):
        string = '[' + ','.join([n2letter(task) for task in self.tasks_done_time]) + ']'
        string += ''.join([f"({core['task']} end at {core['task_end_time']})" for core in self.cores.values()])
        return string
    
    def is_solved(self):
        '''Return whether a node is a full schedule'''
        return len(self.tasks_done_time) == self.task_count
    
    def successors(self):                     
        '''Create and return list of child node of self'''
        childs = list()
        
        #On regarde toutes les tâches qu'on va tenter de rajouter
        for task, info in self.graph.tasks.items():
            
            #On passe les taches déjà ajoutées
            if task in self.tasks_done_time: 
                continue
            
            #On ne garde que les taches dont toutes les dépendances ont été réalisées
            if not all([task_required in self.tasks_done_time for task_required in info['Dependencies']]): 
                continue
            
            #On calcul le temps ou toutes les dépendances de task seront terminés par les coeurs   
            time_all_tasks_done = max([0] + [self.tasks_done_time[task_required] for task_required in info['Dependencies']])
                                         
            for core_n, core in self.cores.items():
                #On ne commence à faire la task que lorsque toutes les dépendances sont calculées et que le core est disponible.
                time_core_available = core["task_end_time"]
                time_task_start = max(time_all_tasks_done, time_core_available)
                
                child = Node(parent = self, task_to_add=task, core_where_to_add=core_n, time_task_start=time_task_start)    
                childs.append(child)
                
        return sorted(childs, key = lambda node: node.f)
        
    def cost(self, child_node):
        '''Return the cost of going from self to child_node, a child node of self
        '''
        res = child_node.g - self.g
        if res < 0:
            raise Exception("Cost difference is negative")
        return res
    
    def h(self):
        '''Estimated remaining time of the node-schedule for reaching a terminal node. Must understimate true value.
        '''
        successor_tasks = list()
        for task, info in self.graph.tasks.items():
            if task in self.tasks_done_time: #On passe les taches déjà ajoutées
                continue
            if not all([task_required in self.tasks_done_time for task_required in info['Dependencies']]):   #On ne garde que les taches dont toutes les dépendances ont été réalisées
                continue
            successor_tasks.append(task)
        if len(successor_tasks) == 0:
            return 0
        return max([self.graph.tasks_to_sbl[task] for task in successor_tasks])
        
    
    #Node-schedule method
    def __lt__(self, node):
        return self.f < node.f
    
    def __hash__(self):
        return int(self.f)
        
    def __eq__(self, node):
        '''Return whether a node is equal to another. Two nodes are considered equal if they have completed the same tasks and if all their cores stop working at same time.
        '''
        if self.g != node.g:
            return False
        if self.tasks_done_time != node.tasks_done_time:
            return False
        return self.set_of_core() == node.set_of_core()
        
    def set_of_core(self):
        return {core["task_end_time"] for core in self.cores.values()}
    
    def compute_g(self):
        return max([core["task_end_time"] for core in self.cores.values()])
    