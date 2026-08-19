def sum_odd_numbers(n: int) -> int:
    total = 0
    for i in range(1, n + 1, 2):
        total += i
    return total

def main():
    while True:
        try:
            n_input = input("\nВведите число N: ").strip()
            
            if not n_input:
                print("Ошибка: Вы ничего не ввели!")
                continue
                
            n = int(n_input)
            
            if n <= 0:
                print("Ошибка: N должно быть положительным числом!")
                continue
                
            result = sum_odd_numbers(n)
            
            print(f"\nСумма всех нечётных чисел от 1 до {n}: {result}")
            
        except ValueError:
            print("Ошибка: Пожалуйста, введите целое число!")
            continue
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана.")
            break
            
        try:
            choice = input("\nХотите вычислить ещё раз? (да/нет): ").lower()
            if choice not in ['да', 'д', 'yes', 'y']:
                print("До свидания!")
                break
        except KeyboardInterrupt:
            print("\nДо свидания!")
            break

if __name__ == "__main__":
    main()
