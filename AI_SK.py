#!/usr/bin/python

import warnings
import sys
import collections

def cross(a, b):
    return [s + t for s in a for t in b]

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """

    # values = []
    # all_digits = '123456789'
    # for c in grid:
    #     if c == '.':
    #         values.append(all_digits)
    #     elif c in all_digits:
    #         values.append(c)

    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    grid_val = dict(zip(boxes, grid))

    for i, j in grid_val.items():
        if j == '.':
            grid_val[i] = '123456789'

    return grid_val

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

    print("====================================================================================")
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
    #solved_values = [box for box in values.keys() if len(values[box]) == 1]

    completed_grids = []
    for i, j in values.items():
        if len(j) == 1:
            completed_grids.append(i)

    #print(len(completed_grids))
    #print(completed_grids)
    for box in sorted(completed_grids):
        digit = values[box]

        #Remove the above digit from its peers
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')

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
                values[dplaces[0]] = digit

    return values

def naked_twins(values):
    """Remove any values in a block where naked twins exists in same unit

    Go through all the units, and whenever there is an occurence of nake twins , remove all the digits in the
    naked twin from other blocks in same unit

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after removing naked twins related digits
    """

    # values['A3'] = '4'
    # values['B3'] = '6'
    # values['C3'] = '8'
    # values['D3'] = '2379'
    # values['E3'] = '379'
    # values['F3'] = '23'
    # values['G3'] = '1'
    # values['H3'] = '5'
    # values['I3'] = '23'
    #test = collections.OrderedDict(sorted(values.items()))

    for unit in unitlist:

        temp_dict = {}
        for box in unit:
            temp_dict[box] = values[box]

        occurrences = collections.Counter(temp_dict.values())
        filtered_dict = {key: value for key, value in temp_dict.items()
                         if occurrences[value] > 1 and len(value) == 2}

        if bool(filtered_dict):
            diff = list(set(temp_dict.keys()) - set(filtered_dict.keys()))

            for digit in (filtered_dict[(list(filtered_dict.keys())[0])]):
                for box in diff:
                    if digit in values[box]:
                        values[box] = values[box].replace(digit, '')
    return values

def reduce_puzzle(values):
    stalled = False
    i = 0
    while (not stalled):
        i = i + 1
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # (sum([len(v) for v in grid_dict.values()])) > 81:
        # print("loop" + str(i))
        values = eliminate(values)
        values = only_choice(values)

        values =   {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

        values = naked_twins(values)

        display(values)
        result_1 = ({'G7': '6', 'G6': '3', 'G5': '2', 'G4': '9', 'G3': '1', 'G2': '8', 'G1': '7', 'G9': '5', 'G8': '4', 'C9': '1',
         'C8': '5', 'C3': '8', 'C2': '237', 'C1': '23', 'C7': '9', 'C6': '6', 'C5': '37', 'A4': '2357', 'A9': '8',
         'A8': '6', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'F6': '125', 'F7': '35', 'F8': '9',
         'F9': '7', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'C4': '4',
         'B8': '3', 'B9': '4', 'I9': '9', 'I8': '7', 'I1': '23', 'I3': '23', 'I2': '6', 'I5': '5', 'I4': '8', 'I7': '1',
         'I6': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'E8': '1', 'A7': '27', 'A6': '257', 'E5': '347',
         'E4': '6', 'E7': '345', 'E6': '579', 'E1': '8', 'E3': '79', 'E2': '37', 'H8': '2', 'H9': '3', 'H2': '9',
         'H3': '5', 'H1': '4', 'H6': '17', 'H7': '8', 'H4': '17', 'H5': '6', 'D8': '8', 'D9': '6', 'D6': '279',
         'D7': '34', 'D4': '237', 'D5': '347', 'D2': '1', 'D3': '79', 'D1': '5'}    )

        result_2 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7',
         'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23',
         'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9',
         'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
         'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125',
         'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '79', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235',
         'F5': '8', 'E2': '3', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17',
         'D3': '79', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6',
         'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

        set_1 = set(values.items())
        set_2 = set(result_1.items())
        set_3 = set(result_2.items())
        #print(set_1 - set_2)
        print(set_1 - set_3)

        #display(values)
        #display(result_2)

        sys.exit(0)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

            # display(grid_dict)

    #print("Final iteration :- " + str(i))
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    # Choose one of the unfilled squares with the fewest possibilities
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    values = reduce_puzzle(values)
    #print("========================================================================================================")
    #display(values)

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

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)

    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]

    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

    diagonal_units = []
    diagonal_units.append([rs + str(rows.index(rs) + 1) for rs in rows])
    diagonal_units.append([rs + str(len(rows) - rows.index(rs)) for rs in rows])

    #Initial Sudoku
    initial_val = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    #initial_val = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    diagonal = True
    if diagonal:
        unitlist = row_units + column_units + square_units + diagonal_units
        initial_val = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        initial_val = '4.......3..9.........1...7.....1.8.....5.9.....1.2.....3...5.........7..7.......8'
        initial_val = '......3.......12..71..9......36...................56......4..67..95.......8......'
    else:
        unitlist = row_units + column_units + square_units

    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

    grid_dict = grid_values(initial_val)
    grid_dict = search(grid_dict)

    if grid_dict:
        display(grid_dict)
    else:
        print("No Soultions "+ str(grid_dict))

    print("========================================================================================================")
    # display({'G7': '8', 'G6': '9', 'G5': '7', 'G4': '3', 'G3': '2', 'G2': '4', 'G1': '6', 'G9': '5',
    #                       'G8': '1', 'C9': '6', 'C8': '7', 'C3': '1', 'C2': '9', 'C1': '4', 'C7': '5', 'C6': '3',
    #                       'C5': '2', 'C4': '8', 'E5': '9', 'E4': '1', 'F1': '1', 'F2': '2', 'F3': '9', 'F4': '6',
    #                       'F5': '5', 'F6': '7', 'F7': '4', 'F8': '3', 'F9': '8', 'B4': '7', 'B5': '1', 'B6': '6',
    #                       'B7': '2', 'B1': '8', 'B2': '5', 'B3': '3', 'B8': '4', 'B9': '9', 'I9': '3', 'I8': '2',
    #                       'I1': '7', 'I3': '8', 'I2': '1', 'I5': '6', 'I4': '5', 'I7': '9', 'I6': '4', 'A1': '2',
    #                       'A3': '7', 'A2': '6', 'E9': '7', 'A4': '9', 'A7': '3', 'A6': '5', 'A9': '1', 'A8': '8',
    #                       'E7': '6', 'E6': '2', 'E1': '3', 'E3': '4', 'E2': '8', 'E8': '5', 'A5': '4', 'H8': '6',
    #                       'H9': '4', 'H2': '3', 'H3': '5', 'H1': '9', 'H6': '1', 'H7': '7', 'H4': '2', 'H5': '8',
    #                       'D8': '9', 'D9': '2', 'D6': '8', 'D7': '1', 'D4': '4', 'D5': '3', 'D2': '7', 'D3': '6',
    #                       'D1': '5'})

    print("end......")