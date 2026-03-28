from functools import reduce

def apply_functions(data, *functions):

    return reduce(lambda result, func: list(map(func, result)), functions, data)

numbers = [1, 2, 3, 4, 5]

def square(x): return x ** 2
def add_ten(x): return x + 10
def double(x): return x * 2

result = apply_functions(numbers, square, add_ten, double)
print(f"Исходный список: {numbers}")
print(f"Результат: {result}")
