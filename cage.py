#! /usr/bin/python2.6


class Cage(object):
	def __init__(self, operator, target):
		self.operator = operator
		self.target = target

class Cages(dict):
	#might be dangerous to depend on values being equal
	def cage_squares(self, cage):
		return [item_square for item_square, item_cage in self.items() if item_cage == cage]
		

def test_square_lookup():
	cage = Cage("+", 2)
	cages = Cages({2:cage, 1:cage})
	assert set(cages.cage_squares(cage)) == set([1, 2])
