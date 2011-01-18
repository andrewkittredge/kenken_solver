#! /usr/bin/python

from cage import Cage
from itertools import permutations

def satisfies_cage_constraint(values, cages):
	'''
	Returns true if a value satisfies the cage constraints
	'''
	square = len(values)
	cage = cages[square]
	square_value = values[square - 1]

	cage_operator = cage.operator
	target = cage.target
	cage_squares = cages.cage_squares(cage)
	num_cage_squares = len(cage_squares)

	if not cage_operator:
		return square_value == target

	else:
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
				
			for permutation in permutations(cage_squares):
				if apply_operator(permutation) == target:
					return True
			return False

def values_already_in_row(choosen_values, dimension):
	end = len(choosen_values) - 1
	squares_back = end % dimension

	values = choosen_values[end - squares_back: end]
	return values

def satisfies_row_constraint(values, dimension):
	'''
	Returns true if the last value in the values list satisfies the
	constraint that no digit is repeated in a row or column.
	'''
	value = values[len(values) - 1]
	used_values = values_already_in_row(values, dimension)
	return value not in used_values

def values_already_in_column(values, dimension):
	previous_value_index = (len(values) - 1) - dimension
	if previous_value_index < 0:
		return []
	else:
		return [values[previous_value_index]] + values_already_in_column(values[0:previous_value_index], dimension)

def satisfies_column_constraint(values, dimension):
	value = values[len(values) - 1]
	return value not in values_already_in_column(values, dimension)
	
def satisfies_grid_constraints(testing_values, dimensions):
	return (satisfies_row_constraint(testing_values, dimensions) and
		satisfies_column_constraint(testing_values, dimensions))

def test_satisfies_grid_constraints():
	assert satisfies_grid_constraints([1, 2, 2, 1], 2) == True
	assert satisfies_grid_constraints([1, 1, 2, 2], 2) == False
	assert satisfies_grid_constraints([1, 2, 3, 2, 3], 3) == True
	assert satisfies_grid_constraints([2, 3, 1, 3, 2, 1], 3) == False
	assert satisfies_grid_constraints([2, 3, 1, 1, 2, 2], 3) == False
	assert satisfies_grid_constraints([1], 3) == True
	assert satisfies_grid_constraints([2], 2) == True


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
	
