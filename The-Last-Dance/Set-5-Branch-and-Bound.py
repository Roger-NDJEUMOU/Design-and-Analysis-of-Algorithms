""" SET 5 - BRANCH AND BOUND """
import math

######## GLOBAL CONSTANTS #########
YES = 1
NO = 0

class Node():
    """ A node is made up of a set of branches that make up the path to it, an upper 
        bound and the cost of getting to it. """
    def __init__(self, path:list, u:float, c:float):
        self.path = path
        self.upper = u
        self.cost = c

    def show(self):
        print("NODE INFO:\n\tPath:[", end="")
        for branch in self.path[1:]: # Don't display the origin as a branch
            branch.show()
        print(f"]\n\tupper: {self.upper}")
        print(f"\tcost: {self.cost}")

class Branch():
    """ A branch consists of an item of the knapsack problem and an integer indicating
        whether this item should be included or not. 1 mean include, 0 means don't include."""
    def __init__(self, b_item:int, include:int):
        self.item = b_item
        self.is_included = include

    def show(self):
        print(f"({self.item}, {self.is_included})", end=" ")


def calc_upper_and_cost(path:list, S:list) -> list:
    """ Calculates the upper bound and cost for the given path """
    # update the status of the last added item
    X = S[:]
    for branch in path:
        X[ branch.item ] = branch.is_included

    upper = 0
    w = 0
    i = 0
    while i < len(Weights) :
        if (w + Weights[i]) <= W and X[i+1] == YES: # only consider included nodes
            upper += (Values[i] * X[i+1])
            w += (Weights[i] * X[i+1])
        i += 1

    cost = upper
    if w < W: # and a fraction of the next item's values
        cost += (W - w) * (Values[i-1] / Weights[i-1])
    
    return [upper, cost]

def get_least_cost_node(L:list) -> Node:
    """ Removes and returns the node with the least cost """
    if len(L) == 1:
        return L.pop()
    LC_node = L[0]
    min_cost = -1 * LC_node.cost
    for node in L[1:]:
        if -1 * node.cost < min_cost:
            LC_node = node
            min_cost = LC_node.cost
    L.remove(LC_node)
    return LC_node


def kill_nodes(L:list, c:float):
    """ Removes all nodes in L that have cost less than 'c' """
    for node in L:
        if node.cost < c :
            L.remove(node)


def should_add_branch(node:Node, n:int) -> bool:
    """ Returns True if 'node' is not the last item of the problem 
        (i.e., 'node' is not a leaf node in the state-space tree) """
    path = node.path
    last_branch = path[-1]
    last_added_item = last_branch.item
    if last_added_item == n :
        return False
    return True


def add_branch(L:list, X:list, parent:Node, left:int):
    """ Adds a branch to the state-space tree from the parent node.
        L is a list of node, X is a list whose values indicate inclusion or exclusion of items. """
    parent_path = parent.path
    last_branch = parent_path[-1]
    new_branch = Branch(b_item=last_branch.item +1, include=left)
    new_path = parent_path + [new_branch]
    upper, cost = calc_upper_and_cost(new_path, X)
    new_node = Node(path=new_path, u=upper, c=cost)
    L.append(new_node)


def knapsack_BB ():
    """ Applies branch-and-bound approach to find the most valuable subset of the items that 
        fit in the knapsack. 
        NB: The items of a given instance be MUST in descending order of their value-to-weight
        ratios. """
    n = len(Weights)
    # Array of inclusion of item: YES means include the item at position i
    X = [ YES for _ in range(n+1) ] 
    X[0] = NO # Exclude the first (empty) node
    starting_path = [ Branch(b_item=0, include=NO) ] # Start from an empty branch
    upper_bound, cost = calc_upper_and_cost(starting_path, X)
    starting_node = Node(path=starting_path, u=upper_bound, c=cost)

    most_valuable = []

    L = [starting_node]

    while L:
        cur_node = get_least_cost_node(L)
        if cur_node.upper >= upper_bound:
            most_valuable = cur_node
            upper_bound = cur_node.upper
            cost = cur_node.cost
            kill_nodes(L, cost)
        if should_add_branch(cur_node, n):
            add_branch(L, X, parent=cur_node, left=YES) # branch in which current node is included
            add_branch(L, X, parent=cur_node, left=NO) # branch in which current node is excluded

    most_valuable.show()


def sort():
    """ Applies selection sort to arranges the items of a given instance of the knapsack 
        problem in descending order by their value-to-weight ratios. This way, the first
        item gives the best payoff per weight unit and the last one gives the worst payoff
        per weight unit: v1/w1 ≥ v2/w2 ≥ .. ≥ vn/wn
    """
    for i in range(len(Weights)-1):
        max_pos = i
        max_ratio = float(Values[i]) / Weights[i]
        for j in range(i+1, len(Weights)):
            ratio = float(Values[j]) / Weights[j]
            if ratio > max_ratio:
                max_pos = j
                max_ratio = ratio
        if max_pos != i :
            Values[i], Values[max_pos] = Values[max_pos], Values[i] # swap values
            Weights[i], Weights[max_pos] = Weights[max_pos], Weights[i] # swap weights



if __name__ == "__main__":
    
    global Weights, Values, W

    # Values = [10, 10, 12, 18]
    # Weights = [2, 4, 6, 9]
    # W = 15
    
    Weights = [7, 5, 4, 3]
    Values = [42, 25, 40, 12]
    W = 10
    
    # Weights = [2, 1, 3, 2]
    # Values = [12, 10, 20, 15]
    # W = 5

    sort()
    print(f"Values:  {Values}")
    print(f"weights: {Weights}")
    knapsack_BB()
