import math


NUM_COLUMN = 9
REMOVE_TOTAL = 10
grid = []
step_counter = 0
solved_moves = []

def num_rows(grid):
    return math.ceil(len(grid) / NUM_COLUMN)


def is_solved(grid):
    return len(get_remaining_numbers(grid)) == 0


def print_grid(grid):
    for i in range(0, num_rows(grid)):
        row = [' ' if x == 0 else str(x) for x in grid[i * NUM_COLUMN:i * NUM_COLUMN + NUM_COLUMN]]
        line = ' '.join(row).ljust(NUM_COLUMN * 2 - 1)
        print("|", line, "|")


def can_remove(grid, index1, index2):
    if index1 == -1 or index2 == -1 or index1 >= len(grid) or index2 >= len(grid):
        return False
    value1 = grid[index1]
    value2 = grid[index2]
    return value1 + value2 == REMOVE_TOTAL or value1 == value2


def get_remaining_numbers(grid):
    return [x for x in grid if x != 0]


def check(grid):
    return grid + get_remaining_numbers(grid)


def check_moves(grid):
    return check_consecutive_elimination(grid) + check_vertical_elimination(grid)


def eliminate(grid, index_pair):
    if index_pair[0] == -1 and index_pair[1] == -1:
        return check(grid)
    grid[index_pair[0]] = 0
    grid[index_pair[1]] = 0
    return grid


def check_consecutive_elimination(grid):
    moves = []
    first_number_index = -1
    second_number_index = -1
    for i in range(0, len(grid)):
        if grid[i] != 0:
            first_number_index = second_number_index
            second_number_index = i
            if can_remove(grid, first_number_index, second_number_index):
                moves.append((first_number_index, second_number_index))
    return moves


def check_vertical_elimination(grid):
    moves = []
    for col in range(0, NUM_COLUMN):
        first_number_index = -1
        second_number_index = -1
        for i in range(0, num_rows(grid)):
            index = i * NUM_COLUMN + col
            if index >= len(grid) or grid[index] == 0:
                continue
            first_number_index = second_number_index
            second_number_index = index
            if can_remove(grid, first_number_index, second_number_index):
                moves.append((first_number_index, second_number_index))
    return moves

def solve(grids):
    global step_counter
    global solved_moves
    step_counter = step_counter + 1
    print("===================================================================")
    print("Move:", step_counter)
    print("Number of grids:", len(grids))
    solved = False
    new_grids = []
    for item in grids:
        grid = item['values']
        existing_moves = item['moves']
        if is_solved(grid):
            print("Solved!")
            print("Moves are ", existing_moves)
            solved = True
            solved_moves = existing_moves
            break
        possible_moves = check_moves(grid)
        if len(possible_moves) == 0:
            new_grids.append({
                'moves': existing_moves + [(-1, -1)],
                'values': check(grid.copy()),
            })
        else:
            for move in possible_moves:
                new_grid_values = eliminate(grid.copy(), move)
                if new_grid_values not in [x['values'] for x in new_grids]:
                    new_grid = {
                        'moves': existing_moves + [move],
                        'values': eliminate(grid.copy(), move),
                    }
                    new_grids.append(new_grid)
    if solved:
        return
    new_grids.sort(key=lambda x: len(get_remaining_numbers(x['values'])))
    solve(new_grids[0:500])


input_grid = "1234567891866582"
# input_grid = "12345678977665"
# input_grid = "1234567891235673215555555555"
# input_grid = "1234567891112131415161718"
# input_grid = "7257559686211582918579776"
# input_grid = input()
grid = [int(x) for x in list(input_grid)]
solve([{ 'moves': [], 'values': grid }])
print_grid(grid)
if solved_moves:
    for i in range(0, len(solved_moves)):
        move = solved_moves[i]
        print('-------------------------- Move', i + 1, move)
        grid = eliminate(grid, move)
        print_grid(grid)
