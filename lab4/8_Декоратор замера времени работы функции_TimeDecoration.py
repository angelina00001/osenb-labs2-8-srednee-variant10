import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {execution_time:.6f} секунд")
        return result
    return wrapper

@timer
def calculate_sum(n):
    return sum(range(1, n + 1))

result = calculate_sum(59)
print(f"Результат: {result}")
