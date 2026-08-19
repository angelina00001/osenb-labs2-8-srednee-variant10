def print_squares_table(max_number):
    rows = (max_number + 9) // 10

    print("   ", end="")
    for units in range(10):
        print(f"{units:6d}", end="")
    print()

    for row in range(rows):
        print(f"{row:2d} ", end="")

        for units in range(10):
            number = row * 10 + units
            if number <= max_number:
                print(f"{number ** 2:6d}", end="")
            else:
                print(" " * 6, end="")
        print()


def main():
    try:
        max_number = int(input("Введите максимальное число для таблицы квадратов: "))

        if max_number < 0:
            print("Пожалуйста, введите неотрицательное число.")
            return

        print(f"\nТаблица квадратов чисел от 0 до {max_number}:")
        print("=" * 65)
        print_squares_table(max_number)

    except ValueError:
        print("Ошибка: пожалуйста, введите целое число.")


if __name__ == "__main__":
    main()
