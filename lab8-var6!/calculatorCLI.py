import argparse


def add_numbers(a, b):
    return a + b


def multiply_numbers(a, b):
    return a * b


def main():
    parser = argparse.ArgumentParser(
        description="Простой калькулятор с CLI интерфейсом",
        epilog="Пример использования: python calculator.py add 5 3"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Доступные команды",
        required=True
    )
    
    parser_add = subparsers.add_parser(
        "add",
        help="Сложить два числа"
    )
    parser_add.add_argument(
        "x",
        type=float,
        help="Первое число"
    )
    parser_add.add_argument(
        "y",
        type=float,
        help="Второе число"
    )
    
    parser_mul = subparsers.add_parser(
        "multiply",
        help="Умножить два числа"
    )
    parser_mul.add_argument(
        "x",
        type=float,
        help="Первое число"
    )
    parser_mul.add_argument(
        "y",
        type=float,
        help="Второе число"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Подробный вывод"
    )

    args = parser.parse_args()

    if args.command == "add":
        result = add_numbers(args.x, args.y)
        operation = "+"
    elif args.command == "multiply":
        result = multiply_numbers(args.x, args.y)
        operation = "*"
    else:
        print(f"Неизвестная команда: {args.command}")
        return
    
    if args.verbose:
        print(f"Операция: {args.x} {operation} {args.y}")
        print(f"Результат: {result}")
    else:
        print(result)


if __name__ == "__main__":
    main()