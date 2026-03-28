class CounterIterator:
    def __init__(self, start=0, end=10, step=1):
        self.current = start
        self.end = end
        self.step = step
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value

  if __name__ == "__main__":
    print(" Простой итератор от 0 до 5 ")
    iterator1 = CounterIterator(0,5)
    for number in iterator1:
        print(number, end=" ")
    print()
    print("\n Итератор с шагом 2 ")
    iterator2 = CounterIterator(0, 10, 2)
    for number in iterator2:
        print(number, end=" ")
    print()
    print("\n Отрицательные числа ")
    iterator3 = CounterIterator(-5, 0)
    for number in iterator3:
        print(number, end=" ")
    print()
    print("\n Ручное использование итератора ")
    iterator4 = CounterIterator(3, 8)
    try:
        while True:
            print(next(iterator4), end=" ")
    except StopIteration:
        print("\nИтерация завершена!")
    print("\n Использование итератора ")
    iterator5 = CounterIterator()
    try:
        while True:
            print(next(iterator5), end=" ")
    except StopIteration:
        print("\nИтерация завершена!")
    print("\n Использование в списке ")
    numbers = list(CounterIterator(1, 6))
    print(f"Список: {numbers}")
