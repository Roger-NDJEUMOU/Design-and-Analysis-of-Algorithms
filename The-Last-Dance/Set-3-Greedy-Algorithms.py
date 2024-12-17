""" 
SET 3 - GREEDY ALGORITHMS 

The greedy approach suggests constructing a solution through a sequence of steps,
each expanding a partially constructed solution obtained so far, until a complete 
solution to the problem is reached. On each step the choice made must be:
-> feasible: it has to satisfy the problem's constraints
-> locally optimal: it has to be the best local choice among all feasible choices
                    available on that step
-> irrevocable: once made, it cannot be changed on subsequent steps of the algorithm
"""
import math


def Kruskal(V:list, E:list, W:list) -> list:
    """ 
    Looks at a minimum spanning tree of a weighted connected graph G=〈V,E〉as an 
    acyclic subgraph with |V|-1 edges for which the sum of the edge weights is the 
    smallest. And constructs a minimum spanning tree as an expanding sequence of 
    subgraphs that are always acyclic but are not necessarily connected on the 
    intermediate stages of the algorithm.
    The algorithm begins by sorting the graph's edges in nondecreasing order of
    their weights. Then, starting with the empty subgraph, it scans this sorted list,
    adding the next edge on the list to the current subgraph if such an inclusion does
    not create a cycle and simply skipping the edge otherwise.        
    """
    tree_edges = []
    encountered = 0
    k = 0
    while encountered < len(V) - 1:
        new_edges = tree_edges + [E[k]]
        if not is_cyclic(V, new_edges):
            tree_edges = new_edges
            encountered += 1
        k += 1
    return tree_edges


def is_cyclic(V:list, E:list) -> bool:
    """ Returns True if the graph G =〈V,E〉contains a cycle, False otherwise. """
    visited = [""] * len(V)
    for v in V:
        if v not in visited:
            index = V.index(v)
            is_cyclic = is_cyclic_helper(V, E, index, visited, "")
            if is_cyclic:
                print("IS_CYCLIC", E)
                return True
    return False


def is_cyclic_helper(V:list, E:list, vertex_index:int, visited:list, parent:str) -> bool :
    """ A cycle in a Graph is a path that starts and ends at the same vertex, where no edges are repeated.  """
    cur_vertex = V[vertex_index]
    visited[vertex_index] = cur_vertex

    for i in range(len(E)):
        if E[i][0] == cur_vertex:
            next_vertex = E[i][1]
            if next_vertex not in visited:
                if is_cyclic_helper(V, E, V.index(next_vertex), visited, cur_vertex):
                    return True
            elif next_vertex != parent:
                return True
    return False
    

def sort_graph(E:list, W:list) :
    """ Sorts the given list in nondecreasing order of edge weight using selection sort. """
    for i in range(len(W)-1):
        min_index = i
        for j in range(i+1, len(W)):
            if W[j] < W[min_index]:
                min_index = j
        if min_index != i:
            E[min_index], E[i] = E[i], E[min_index]
            W[min_index], W[i] = W[i], W[min_index] 


def Prim(V: list, E:list, W:list) -> list:
    """ Constructs a minimum spanning tree through a sequence of expanding subtrees. 
        The initial subtree in such a sequence consists of the first vertex of the set 
        of vertices. On each iteration, the algorithm expands the current tree in the 
        greedy manner by simply attaching to it a vertex not in the tree connected to a 
        vertex in the tree by an edge of the smallest weight. The algorithm stops after 
        all the graph's vertices have been included in the tree being constructed.  """
    tree_vertices = [V[0]]
    tree_edges = []
    for i in range(1,len(V)):
        min_weight = math.inf
        min_vertex = None
        min_edge = None
        for j in range(len(E)):
            if E[j][0] in tree_vertices and E[j][1] not in tree_vertices and W[j] < min_weight:
                min_weight = W[j]
                min_vertex = E[j][1]
                min_edge = E[j]
            elif E[j][1] in tree_vertices and E[j][0] not in tree_vertices and W[j] < min_weight:
                min_weight = W[j]
                min_vertex = E[j][0]
                min_edge = E[j]
        if min_vertex is None or min_vertex in tree_vertices:
            continue
        tree_vertices.append(min_vertex)
        tree_edges.append(min_edge)
    
    return [tree_vertices, tree_edges]



def change_making_optimized(amount:int, denoms:list) -> list:
    """ Finds the optimal solution to the change making problem, 
        i.e., the solution with the least number of coins.
        At each step, i, 
        -> determine all feable solutions using denominations d1,d2,...,d_i
        -> finds the optimal solution of all the feasible solutions
        Thus, the optimal solution at step i = len(denom)-1 will be the optimal 
        solution to the problem.
    """
    # Getting all feasible solutions
    solutions = [] # array to store all feasible solutions
    min = math.inf
    optimal_solution = None # Store only the optimal solution after each step

    for i in range(len(denoms)):
        if amount % denoms[i] == 0:
            coins = amount // denoms[i]
            solution = [(coins, denoms[i])]
            solutions.append([coins, solution])
            if coins < min:
                min = coins
                optimal_solution = solution
        n = amount
        sub_amount = 0
        coins = 0
        partial_denoms = []
        for j in range(i+1):
            if n >= denoms[j]:
                coin = n // denoms[j]
                coins += coin
                n %= denoms[j]
                sub_amount += coin * denoms[j]
                partial_denoms.append((coin, denoms[j]))
                
            if sub_amount == amount:
                solutions.append([coins, partial_denoms])
                if coins < min:
                    min = coins
                    optimal_solution = partial_denoms
   
    return [optimal_solution, solutions]


def change_making(amount: int, denoms:list) -> list:
    """ Give change for a specific 'amount' with the least number of coins 
        of the denominations, 'denom'=[d1,d2,...,dm],where d1 > d2 >...> dm.
        This function applies the brute-force appoach. """
    change = []
    for d in denoms:
        if amount >= d:
            n = amount // d
            amount %= d
            change.append((n, d))
    
    return change


if __name__ == "__main__":
    # # Prim'a Algorithm: Test case 3
    # vertices =['a','b','c','d','e']
    # edges = [('a','b'),('a','c'),('a','e'),('b','d'),
    #          ('b','e'),('c','e'),('c','d'),('d','e')]
    # weights = [5,7,2,6,3,4,4,5]
    # sort_graph(E=edges,W=weights)
    # print(Kruskal(V=vertices, E=edges, W=weights))
    # # print(Prim(V=vertices, E=edges, W=weights)[1])

    # Prim'a Algorithm: Test case 2
    vertices = ['a','b','c','d','e','f'] 
    edges = [('a','b'),('a','f'),('a','e'),('b','c'),
             ('b','f'),('c','d'),('c','f'),('d','e'),
             ('d','f'),('e','f')
             ] 
    weights = [3,5,6,1,4,6,4,8,5,2] 
    
    sort_graph(E=edges,W=weights)
    print(Kruskal(V=vertices, E=edges, W=weights))
    print(Prim(V=vertices, E=edges, W=weights)[1])

    # Prim'a Algorithm: Test case 1
    # vertices = ['a','b','c','d']
    # edges = [('a','b'),('a','c'),('a','d'),('c','d')]
    # weights = [1, 5, 2, 3]
    # sort_graph(E=edges,W=weights)
    # print(Prim(V=vertices, E=edges, W=weights)[1])
    # print(Kruskal(V=vertices, E=edges, W=weights))

    # amount = 30
    # denominations = [25, 10, 1]

    # optimal_solution, all_solutions = change_making_optimized(amount, denominations)
    # print(f"Optimal solution: \t {optimal_solution}")
    # print(f"Feasible solution: \t{all_solutions}")

    # print(change_making(amount, denominations))
