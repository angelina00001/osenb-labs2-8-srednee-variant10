from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_numbers_comp = [x for x in numbers if x % 2 == 0]
print("list comprehension:", even_numbers_comp)
