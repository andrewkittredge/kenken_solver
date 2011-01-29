#! /Library/Frameworks/Python.framework/Versions/2.6/bin/python
DEBUG = True

from constraint_solvers import remaining_square_values, satisfies_cage_constraint
from cage import Cage, Cages
from operator import add, sub, mul, div
cages = {}

def satisfying_values(previous_values, cages, dimension):
	number_squares = dimension ** 2
	if len(previous_values) == number_squares:
		#All squares have been decided
		yield []

	else:
		for possible_value in remaining_square_values(
							previous_values,
							dimension):
			working_list = previous_values + [possible_value]
			if satisfies_cage_constraint(working_list, cages):
				for subsequent_values in satisfying_values(
			                        				working_list, 
							                        cages, 
							                        dimension):
					yield [possible_value] + subsequent_values

def test_satisfying_values():
	return satisfying_values([], 3)


def test_four_by_four():
    solution_from_web = [3,1,2,4,2,3,4,1,4,2,1,3,1,4,3,2]
    cage_1 = Cage(mul, 18)
    cage_2 = Cage(div, 2)
    cage_3 = Cage(sub, 3)
    cage_4 = Cage(sub, 3)
    cage_5 = Cage(add, 7)
    cage_6 = Cage(sub, 1)
    cage_7 = Cage(sub, 1)

    cages = Cages({1: cage_1,
                   2: cage_2,
                   3: cage_2,
                   4: cage_3,
                   5: cage_1,
                   6: cage_1,
                   7: cage_4,
                   8: cage_3,
                   9: cage_5,
                   10: cage_5,
                   11: cage_4,
                   12: cage_6,
                   13: cage_5,
                   14: cage_7,
                   15: cage_7,
                   16: cage_6})

    import pdb
    pdb.set_trace()
    solutions = satisfying_values([], cages, 4)
    assert solution_from_web in solutions

def four_by_four():
	cage_1 = Cage(add, 7)
	cage_2 = Cage(mul, 8)
	cage_3 = Cage(add, 4)
	cage_4 = Cage(sub, 2)
	cage_5 = Cage(sub, 1)
	cage_6 = Cage(mul, 12)
	cage_7 = Cage(div, 2)
	cages = Cages({1: cage_1,
			2: cage_1,
			3: cage_2,
			4: cage_2,
			5: cage_3,
			6: cage_4,
			7: cage_2,
			8: cage_5,
			9: cage_3,
			10: cage_4,
			11: cage_6,
			12: cage_5,
			13: cage_7,
			14: cage_7,
			15: cage_6,
			16: cage_6})
	if DEBUG:
		import pdb
		#pdb.set_trace()
	solutions = satisfying_values([], cages, 4)
	print solutions.next()



def test_with_cage():
	cage_1 = Cage(add, 3)
	cage_3 = Cage(None, 2)
	cage_4 = Cage(None, 1)
	cages = Cages({1: cage_1, 2: cage_1, 3: cage_3, 4: cage_4})
	solutions = satisfying_values([], cages, 2)
	first_solution = solutions.next()
	print first_solution
	assert first_solution  == [1, 2, 2, 1]

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

if "__name__" == "__main__":
    test_four_by_four()
