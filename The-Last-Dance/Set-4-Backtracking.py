""" SET 4 - BACKTRACKING """

def n_queens(n:int):
    """ Applies DFS to find all feasible solutions to the problem is to place n queens
    on an n x n chessboard so that no two queens attack each other by being in the same
    row or in the same column or on the same diagonal.  """

    global Visited
    global Solutions

    if n == 1:
        Solutions.append([n])
        return
    if n == 2 or n == 3 or n < 1:
        return
    for i in range(1, n+1):
        if len(Visited) == n: # We have found a solution
            bounded = n_queens_bound(Visited[-3], Visited[-2])
            if not bounded:
                Solutions.append(Visited)
        Visited = []
        n_queens_solver(n, [i])
    

def n_queens_solver(n:int, stack:list):
    """ Perform DFS on a single branch """
    global Visited
    global Solutions

    cur_pos = stack.pop()
    Visited.append(cur_pos)
    remaining_positions = [x for x in range(1, n+1) if x not in Visited]
    for pos in remaining_positions:
        bounded = n_queens_bound(cur_pos, pos)
        if not bounded:
            stack.append(pos)
            n_queens_solver(n, stack)
            

def n_queens_bound(cur_pos:int, to_pos:int) -> bool:
    adj_to_cur_pos = [cur_pos-1, cur_pos+1]
    if to_pos in adj_to_cur_pos:
        return True
    return False

if __name__ == "__main__" :
    Visited = []
    Solutions = []

    n_queens(4)

    # print(Visited)
    print(Solutions)
