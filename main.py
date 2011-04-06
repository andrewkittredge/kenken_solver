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
    solution_from_web = [4,1,2,4,2,3,4,1,4,2,1,3,1,4,3,2]
    cage_1 = Cage(mul, 18)
    cage_2 = Cage(div, 2)
    cage_3 = Cage(sub, 3)
    cage_4 = Cage(sub, 3)
    cage_5 = Cage(add, 7)
    cage_6 = Cage(sub, 1)
    cage_7 = Cage(sub, 1)
    print True

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
	
def test_seven_by_seven():
    cage1 = Cage(sub, 2)
    cage2 = Cage(mul, 30)
    cage3 = Cage(sub, 2)
    cage4 = Cage(None, 1)
    cage5 = Cage(sub, 3)
    cage6 = Cage(sub, 3)
    cage7 = Cage(add, 12)
    cage8 = Cage(sub, 3)
    cage9 = Cage(add, 14)
    cage10 = Cage(add, 5)
    cage11 = Cage(add, 8)
    cage12 = Cage(sub, 5)
    cage13 = Cage(None, 2)
    cage14 = Cage(sub, 1)
    cage15 = Cage(sub, 5)
    cage16 = Cage(add, 11)
    cage17 = Cage(add, 11)
    cage18 = Cage(None, 7)
    cage19 = Cage(mul, 12)
    cage20 = Cage(add, 10)
    cage21 = Cage(sub, 1)
    cage22 = Cage(div, 3)
    cage23 = Cage(mul, 15)
    cage24 = Cage(sub, 2)
    
    cages = Cages({
				   1: cage1,
				   2: cage2,
				   3: cage3,
				   4: cage3,
				   5: cage4,
				   6: cage5,
				   7: cage5,
				   
				   8: cage1,
				   9: cage2,
				   10: cage2,
				   11: cage6,
				   12: cage6,
				   13: cage7,
				   14: cage8,
				   
				   15: cage9,
				   16: cage9,
				   17: cage9,
				   18: cage10,
				   19: cage10,
				   20: cage7,
				   21: cage8,
				   
				   22: cage11,
				   23: cage12,
				   24: cage13,
				   25: cage14,
				   26: cage14,
				   27: cage7,
				   28: cage15,
				   
				   29: cage11,
				   30: cage12,
				   31: cage16,
				   32: cage16,
				   33: cage17,
				   34: cage17,
				   35: cage15,
				   
				   36: cage18,
				   37: cage19,
				   38: cage20,
				   39: cage21,
				   40: cage22,
				   41: cage22,
				   42: cage23,
				   
				   43: cage19,
				   44: cage19,
				   45: cage20,
				   46: cage21,
				   47: cage24,
				   48: cage24,
				   49: cage23
				   })
    print list(satisfying_values([], cages, 7))
    
    
four_by_four()
test_seven_by_seven()
if "__name__" == "__main__":
    test_four_by_four()
    print 'done'
