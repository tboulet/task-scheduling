
import task_graph_generator
import mpi4py

def search(stack, bound, depth):
    indexes = [0]
    while (len(stack)):
        node = stack[-1]
        index = indexes[-1]

        f = node.g + graph.h(node)

        if graph.is_solved(node):
            return sorted(graph.successors(stack[-2]), key=lambda n: n.g)[0]
        
        if len(stack) == depth:
            return sorted(graph.successors(stack[-2]), key=lambda n: n.g + graph.h(n))[0]

        if f > bound:
            stack.pop()
            indexes.pop()
            continue

        if index >= graph.n_successors(node):
            stack.pop()
            indexes.pop()
            continue
        
        succ = graph.successor(node, index)
        indexes[-1] = index + 1
        stack.append(succ)
        indexes.append(0)
    
    return False


def ida_star(depth = np.inf):
    bound = graph.h(graph.root)*2
    stack = [graph.root]
    t = search(stack, bound, depth)
    if isinstance(t, Node):
        print('Done')
        return t
    print('Not found')
    return None


def main():
    DAG = task_graph_generator.generate_task_graph(10, 1, 1000, 300)
    
    pass

if __name__ == "__main__":
    main()