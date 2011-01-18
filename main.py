#! /usr/bin/python2.6

from constraint_solvers import satisfies_grid_constraints
from constraint_solvers import satisfies_cage_constraint
from cage import Cage, Cages
from operator import add, sub, mul
cages = {}

def satisfying_values(previous_values, cages, dimension):
	number_squares = dimension ** 2
	if len(previous_values) == number_squares:
		#All squares have been decided
		yield previous_values

	else:
		possible_values = range(1, dimension + 1)
		for possible_value in possible_values:
			new_list = previous_values + [possible_value]

			grid_constraint = satisfies_grid_constraints(
					new_list, dimension)

			cage_constraint = satisfies_cage_constraint(
					new_list, cages)

			if (grid_constraint and cage_constraint):
				for satisfying_value in satisfying_values(
						new_list, cages, dimension):
					yield satisfying_value

def test_satisfying_values():
	return satisfying_values([], 3)

def test_with_cage():
	cage_1 = Cage(add, 3)
	cage_3 = Cage(None, 2)
	cage_4 = Cage(None, 1)
	cages = Cages({1: cage_1, 2: cage_1, 3: cage_3, 4: cage_4})
	assert satisfying_values([], cages, 2).next() == [1, 2, 2, 1]

	cage_2 = Cage(sub, 1)
	cages[1] = cage_2
	cages[2] = cage_2
	assert satisfying_values([], cages, 2).next() == [1, 2, 2, 1]

	cage = Cage(mul, 4)
	cages[1] = cage
	cages[4] = cage
	cages[2] = Cage(None, 1)
	cages[3] = Cage(None, 1)
	assert satisfying_values([], cages, 2).next() == [2, 1, 1, 2]
