class Counter:
    def __init__(self, initial_value=0):
        self.__count = initial_value
    
    def increment(self):
        self.__count += 1
    
    def decrement(self):
        self.__count -= 1
    
    def get_count(self):
        return self.__count
    
    def reset(self):
        self.__count = 0

if __name__ == "__main__":
    counter = Counter()
    print("Тест класса-счётчика:")
    print(f"Начальное значение: {counter.get_count()}")
    counter.increment()
    counter.increment()
    print(f"После двух увеличений: {counter.get_count()}")
    counter.decrement()
    print(f"После уменьшения: {counter.get_count()}")
    counter.reset()
    print(f"После сброса: {counter.get_count()}")
