""" 
SET 2 - DYNAMIC PROGRAMMING 

Principle of optimality: 
    An optimal solution to any instance of an optimization problem 
    is composed of optimal solutions to its subinstances.
"""
import random

def MF_knapsack(i:int, j:int):
    """ Implements the memory function method for the knapsack problem
    Input: A nonnegative integer i indicating the number of the first
        items being considered and a nonnegative integer j indicating
        the knapsack capacity
    Output: The value of an optimal feasible subset of the first i items
    NB: Uses as global variables input arrays Weights[1..n], Values[1..n],
        and table F [0..n, 0..W] whose entries are initialized with -1's except for
        row 0 and column 0 initialized with 0's
    """
    global F
    global Weights
    global Values

    if F [i][j] < 0:
        if j < Weights[i-1]:
            value = MF_knapsack(i-1, j)
        else:
            value = max(MF_knapsack(i-1, j),  Values[i-1] + MF_knapsack(i-1, j-Weights[i-1]))
        F [i][j] = value
    return F[i][j]


def knapsack(weights:list, values:list, W:int) -> list:
    """ Applies dynamic programming approach to find the most valuable subset
        of the items that fit into the knapsack.  
    """
    n = len(weights)
    F = [] # Matrix to contain optimal solutions to all instances of the problem
    for i in range(n+1):
        F.append([0 for _ in range(W+1)])

    print(F[0])
    for i in range(1, n+1):
        for j in range(1,W+1):
            aux = j - weights[i-1]
            if aux >= 0:
                F[i][j] = max(F[i-1][j], values[i-1] + F[i-1][aux])
            else:
                F[i][j] = F[i-1][j]
        print(F[i])

    selected_items = get_optimal_subset(W, weights, F)

    return [F[n][W], selected_items]


def get_optimal_subset(W:int, weights:list, F: list) -> list:
    """ find the composition of an optimal subset by backtracing the 
        computations of the table, F. """
    n = len(weights)
    items = [i for i in range(1, n+1)]
    selected_items = []
    w = W
    for i in range(n, 0, -1):
        if F[i][w] != F[i-1][w]:
            selected_items.append(items[i-1])
            w -= weights[i-1]

    return selected_items

def coin_row(C:list, n:int) -> int:
    """ Applies formula (8.3 below) to find the maximum amount of money that 
        can be picked up from a coin row without picking two adjacent coins.
        
        F (i) = max{c_i + F (i-2), F (i-1)} for i = 2,3,...,n
        F (0) = 0, F (1) = c_1.                                   (8.3)
    """
    F = list([-1] * (n + 1))
    F[0] = 0
    F[1] = C[0]
    
    for i in range(2, n+1):
        F[i] = max(C[i-1] + F[i-2], F[i-1])
    return F[n]


def fibonacci(n:int):
    """ Computes the nth Fibonacci number iteratively using the formula below
        F (i) = F(i-1) + F(i-2) for i = 2,3,...n
        F(0) = 0, F (1) = 1
    """
    F = list( [-1] * (n+1) )
    F[0] = 0
    F[1] = 1

    for i in range(2, n+1):
        F[i] = F[i-1] + F[i-2]
    return F[n]


def robot_coin_collection(board:list) -> int:
    """ Applies dynamic programming to compute the largest number of
        coins a robot can collect on an n x m board by starting at (1, 1)
        and moving right and down from upper left to down right corner.
    """
    n = len(board) 
    m = len(board[0]) 
    # Build the result board with the first row and first column values set to 0
    F = [[0] * (m + 1)]
    [F.append([0] + board[i]) for i in range(n)]

    for i in range(1, n+1):
        for j in range(1, m+1):
            has_coin = 1 if F[i][j] else 0
            F[i][j] = max(F[i-1][j], F[i][j-1]) + has_coin
    
    return F[n][m]


if __name__ == "__main__":
    Weights = [2, 1, 3, 2]
    Values = [12, 10, 20, 15]
    capacity = 5

    # Weights = [7, 3, 4, 5]
    # Values = [42, 12, 40, 25]
    # capacity = 10

    nb_items = len(Weights)
    col = capacity + 1
    row = nb_items + 1
    F = [[0 for _ in range(col)]]
    for i in range(row) :
        F.append([-1 for _ in range(col)])
        F[i+1][0]=0

    optimal_value = MF_knapsack(i=nb_items, j=capacity)
    [print(F[i]) for i in range(row)]
    print(f"Optmial value: {optimal_value}")
    selected_items = get_optimal_subset(W=capacity, weights=Weights, F=F)
    print(f"Optmial items: {selected_items}")

    # optimal_value, items = knapsack(weights=Weights, values=Values, W=capacity)
    # print(f"Optmial value: {optimal_value}")
    # print(f"Optmial items: {items}")

    # coins = [5, 1, 2, 10, 6, 2]
    # print(f"The maximum amount of money that can be picked up is : {coin_row(coins, len(coins))}")

    # print(f"Fibo(5) = {fibonacci(5)}")
    
    # coin_board = [[0,0,0,0,5,0],
    #               [0,2,0,4,0,0],
    #               [0,0,0,4,0,6],
    #               [0,0,3,0,0,6],
    #               [1,0,0,0,5,0]]
    # for i in range(len(coin_board)):
    #     print(coin_board[i])
    # print(f"Largest number of coins: {robot_coin_collection(coin_board)}")
    
