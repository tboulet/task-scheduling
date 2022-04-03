# Task-scheduling with A* and IDA*

Implementation of an informed search algorithm A* and IDA* for solving a scheduling problem, aiming to optimize the use of several cores for completing interdependent tasks.

![alt text](https://github.com/tboulet/task-scheduling/blob/main/results/xsmallComplex_6_h.png?raw=true)


If you want use our algorithm, you have to create a config file in scripts/config.py where you can specify the number of cores and the task graph of your problem. A template is available at scripts/config_template.py.

Then put the task graph json file in at the path corresponding to the config. The json file should be of the form (for a very simple graph):

  
    {
        "nodes": {
          "1": {
            "Data": "00:47:23.6552354",
            "Dependencies": []
          },
          "2": {
            "Data": "01:00:56.0712509",
            "Dependencies": [
              1
            ]
          },
          "3": {
            "Data": "00:45:41.9822376",
            "Dependencies": [
              1
            ]
          }
        }
      }

The number represents tasks, the Data value their duration and the Dependencies the tasks necessary to start being computed.

Please then run :
    
    python scripts/main.py

It will plot an optimized schedule and save the solution at the same path. The solution is a json file of the form:

    {"1": [0, 2843, 0], "3": [2843, 5584, 0], "2": [2843, 6499, 1]}

The number represents tasks and each list [start, end, core] represents the starting time of the computation of a task, the ending time and finally the core on which it should be computed according to the optimal solution.
    
