import sys
sys.path.append('../aima-python')
from search import *

class Cached_Node(Node):
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.cached_value = None
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Cached_Node {}>".format(self.state)

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Cached_Node(next_state, self, action,
                         problem.path_cost(self.path_cost, self.state,
                                           action, next_state))
        return next_node

    def __eq__(self, other):
        return isinstance(other, Cached_Node) and self.state == other.state

def memoize(fn, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list. """
    def memoized_fn(obj, *args):
        if obj.cached_value:
            print('Found')
            return obj.cached_value
        else:
            print('Setting')
            val = fn(obj, *args)
            obj.cached_value = val
            return val
    return memoized_fn

def cached_best_first_graph_search(problem, f):
    f = memoize(f, 'f')
    node = Cached_Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def fixed_astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h)
    return cached_best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def best_first_tree_search(problem, f):
    f = memoize(f, 'f')
    node = Cached_Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if child in frontier:
                frontier.append(child)
                #if f(child) < frontier[child]:
                    #del frontier[child]
                    #frontier.append(child)
    return None

def astar_tree_search(problem, h=None):
    h = memoize(h or problem.h)
    return best_first_tree_search(problem, lambda n: n.path_cost + h(n))

def depth_limited_graph_search(problem, limit=50):
    explored = []
    def graph_recursive_dls(node, problem, limit, explored):
        if node.state in explored:
            return None
        else:
            explored.append(node.state)
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = graph_recursive_dls(child, problem, limit - 1, explored)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    return graph_recursive_dls(Node(problem.initial), problem, limit, explored)


def iterative_deepening_graph_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_graph_search(problem, depth)
        if result != 'cutoff':
            return result