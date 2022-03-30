import numpy as np
from solution_check import check_solution
from tasks_reader import *



class Node():
    def __init__(self, tasks_in_progress, processor, task):
        tasks_done = []
        tasks_in_progress = {}
        self.processor = processor
        self.task = task
        return
    def generate_childs():
        childs = []
        for i in tasks:
            pass


def get_border_tasks(tasks):
    begin_tasks = []
    end_tasks = []
    for i in tasks:
        if len(tasks[i].childs) == 0:
            end_tasks.append(i)
        if len(tasks[i].parents) == 0:
            begin_tasks.append(i)
    return begin_tasks, end_tasks


def save_static_bottom_level(task : Task):
    if task_is_terminal(task):
        task.sbl = task.duration
    else:
        list_sbl_child = list()
        for task_child in task.childs:
            if tasks[task_child].sbl != inf:
                sbl_child = tasks[task_child].sbl
            else:
                sbl_child = save_static_bottom_level(tasks[task_child])
            list_sbl_child.append(sbl_child)
        task.sbl = max(list_sbl_child) + task.duration
    return task.sbl

def task_is_terminal(task):
    return len(task.childs) == 0

def compute_bottom_level(tasks: list()):
    for task in tasks:
        save_static_bottom_level(tasks[task])
    return


def main():
    global tasks
    tasks = read_data("../Graphs/smallRandom.json")
    begin_tasks, end_tasks = get_border_tasks(tasks)
    compute_bottom_level(tasks)
    print(begin_tasks, end_tasks)
    check_solution(None, "../Graphs/smallRandom.json")

if __name__ == "__main__":
    main()