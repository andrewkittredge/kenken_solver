#! /usr/bin/python

from cage import Cage
from itertools import permutations

def satisfies_cage_constraint(values, cages):
    '''
    Returns true if a value satisfies the cage constraints
    '''

    square = len(values)
    square_value = values[square - 1]

    cage = cages[square]
    cage_operator = cage.operator
    target = cage.target

    if not cage_operator:
        return square_value == target

    else:
        cage_squares = cages.cage_squares(cage)
        num_cage_squares = len(cage_squares)

        if square != max(cage_squares):
            #Only work the constraint if all other values in the
            #cage have been decided.
            #TODO: Make this function smarter. ie. realize when no 
            #subsequent value will sastisfy the constraint
            return True
        else:
            def apply_operator(squares_values):
                if len(squares_values) == 2:
                    return cage_operator(squares_values[0],
                              squares_values[1])
                else:
                    return cage_operator(squares_values[0], 
                    apply_operator(squares_values[1:]))
                
            check_values = [values[cage_square - 1] for cage_square in cage_squares]
            #this is less that optimal
            for permutation in permutations(check_values):
                if apply_operator(permutation) == target:
                    return True
            return False

def values_already_in_row(choosen_values, dimension):
    end = len(choosen_values)
    squares_back = end % dimension

    values = choosen_values[end - squares_back: end]
    return values


def values_already_in_column(values, dimension):
    previous_value_index = len(values) - dimension
    if previous_value_index < 0:
        return []
    else:
        return [values[previous_value_index]] + values_already_in_column(values[0:previous_value_index], dimension)

def remaining_square_values(values, dimension):
    possible_values = set(range(1, dimension + 1))
    column_values = values_already_in_column(values, dimension)
    row_values = values_already_in_row(values, dimension)
    ineligible_values = set(column_values + row_values)

    return possible_values - ineligible_values

def test_cage():
    from operator import add, mul
    from cage import Cages
    import pdb
    c = Cage(add, 10)
    cs = Cages({1: c, 2: c, 3: c, 4: c})
    assert satisfies_cage_constraint([1,2,3,4], cs)
    assert not satisfies_cage_constraint([25,2,2,2], cs)
    c = Cage(mul, 15)
    cs = Cages({1: c, 2: c, 3: c})
    pdb.set_trace()
    assert satisfies_cage_constraint([1, 3, 5], cs)


def test_values_already_in_column():
    assert values_already_in_column([], 2) == []
    assert values_already_in_column([1], 2) == []
    assert values_already_in_column([1, 2], 2) == [1]
    assert values_already_in_column([1, 2, 2], 2) == [2]
    assert set(values_already_in_column([1, 2, 3, 2, 3, 1], 3)) == set([1, 2])

def test_values_already_in_row():
    assert values_already_in_row([], 2) == []
    assert values_already_in_row([1], 2) == [1]
    assert values_already_in_row([1, 2], 2) == []
    assert set(values_already_in_row([1, 3], 3)) == set([1, 3])
    assert set(values_already_in_row([1, 2, 3, 1, 2], 3)) == set([1, 2])

def test_remaining_square_values():
    assert set(remaining_square_values([], 2)) == set([1, 2])
    assert set(remaining_square_values([1], 2)) == set([2])
    assert set(remaining_square_values([1, 2], 2)) == set([1, 2])
    assert set(remaining_square_values([1, 2, 3], 3)) == set([1, 2, 3])

def test_satisfies_grid_constraints():
    assert satisfies_cage_constraint([1, 2, 2, 1], 2) == True
    assert satisfies_grid_constraint([1, 1, 2, 2], 2) == False
    assert satisfies_grid_constraint([1, 2, 3, 2, 3], 3) == True
    assert satisfies_grid_constraint([2, 3, 1, 3, 2, 1], 3) == False
    assert satisfies_grid_constraint([2, 3, 1, 1, 2, 2], 3) == False
    assert satisfies_grid_constraint([1], 3) == True
    assert satisfies_grid_constraint([2], 2) == True


def test_satisfies_column_constraint():
    assert satisfies_column_constraint([1, 2, 1, 2], 2) == False
    assert satisfies_column_constraint([1, 2, 2, 1], 2) == True
    assert satisfies_column_constraint([1, 2], 2) == True
    assert satisfies_column_constraint([1, 2, 2], 2) == True
    assert satisfies_column_constraint([1, 2, 3, 2, 1], 3) == True
    assert satisfies_column_constraint([1, 3, 2, 2, 1, 2], 3) == False
    assert satisfies_column_constraint(
            [1, 2, 3, 3, 1, 2, 2, 3, 1], 3) == True
    assert satisfies_column_constraint([1], 3) == True


def test_satisfies_row_constraint():
    assert satisfies_row_constraint([1, 2, 2, 1], 2) == True
    assert satisfies_row_constraint([1, 1, 2, 2], 2) == False
    assert satisfies_row_constraint([1, 1], 2) == False
    assert satisfies_row_constraint([2, 1, 1], 2) == True
    assert satisfies_row_constraint([2, 1, 3], 3) == True
    assert satisfies_row_constraint([2, 1, 3, 1, 1], 3) == False
    assert satisfies_row_constraint([3, 1, 2, 1, 2], 3) == True
    assert satisfies_row_constraint([3], 3) == True
    assert satisfies_row_constraint([2], 2) == True


def test_cage_lookup():
    cage = Cage("+", 2)
    cages = {1: cage, 2: cage}
