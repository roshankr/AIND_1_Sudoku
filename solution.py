
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:

        #create a dictionary for unitlist
        temp_dict = {}
        for box in unit:
            temp_dict[box] = values[box]

        #identify the naked twins from dictionary
        import collections
        occurrences = collections.Counter(temp_dict.values())
        filtered_dict = {key: value for key, value in temp_dict.items()
                         if occurrences[value] > 1 and len(value) == 2}

        #If any naked twins exists, then create a dictionary of all ellements except naked twins.
        #Loop through this new dictionary and remove any digits (digits from nakeD twins)
        if bool(filtered_dict):
            diff = list(set(temp_dict.keys()) - set(filtered_dict.keys()))

            for digit in (filtered_dict[(list(filtered_dict.keys())[0])]):
                for box in diff:
                    if digit in values[box]:
                        assign_value(values, box, values[box].replace(digit, ''))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    grid_val = dict(zip(boxes, grid))

    for i, j in grid_val.items():
        if j == '.':
            assign_value(grid_val, i, '123456789')

    return grid_val


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    completed_grids = []
    for i, j in values.items():
        if len(j) == 1:
            completed_grids.append(i)

    for box in sorted(completed_grids):
        digit = values[box]

        #Remove the above digit from its peers
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            #if only one box exists with a specific digit , then replace its value, else skip
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() , only_choice() and naked_twins(). If at some point, there is a box with no
    available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    stalled = False
    i = 0
    while (not stalled):
        i = i + 1
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    # Choose one of the unfilled squares with the fewest possibilities
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    values = reduce_puzzle(values)

    if values==False:
        return False
    elif (sum([len(v) for v in values.values()])) == 81:
        return values
    else:
        grid ="123456789"
        grid_len = len(grid)
        for i, j in values.items():
            if len(j) > 1 and len(j) < grid_len:
                grid_len = len(j)
                grid = i

        for grid_val in values[grid]:
            sudoku_temp = values.copy()
            sudoku_temp[grid] = grid_val
            attempt = search(sudoku_temp)
            if attempt:
                return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    global boxes, rows, cols,peers,unitlist

    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)

    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]

    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

    # Add diagonal elements also to unitlist for diagonal sudoku
    diagonal_units = []
    diagonal_units.append([rs + str(rows.index(rs) + 1) for rs in rows])
    diagonal_units.append([rs + str(len(rows) - rows.index(rs)) for rs in rows])

    unitlist = row_units + column_units + square_units + diagonal_units

    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
    values = grid_values(grid)
    values = search(values)

    if values:
        return values
    else:
        return False

if __name__ == '__main__':
    #Not a diagonal Sudoku
    #diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

    #diaginal sudoku's
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '4.......3..9.........1...7.....1.8.....5.9.....1.2.....3...5.........7..7.......8'
    #diag_sudoku_grid = '......3.......12..71..9......36...................56......4..67..95.......8......'

    status = solve(diag_sudoku_grid)

    if status:
        display(status)
    else:
        print("No Solution for this sudoku")

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')