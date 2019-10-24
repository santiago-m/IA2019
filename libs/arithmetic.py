import math

def is_perfectsquare(number):
	root = math.sqrt(number)
	return int(root + 0.5) ** 2 == number