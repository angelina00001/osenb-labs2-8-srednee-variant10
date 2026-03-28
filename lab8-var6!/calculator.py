#!/usr/bin/env python3
"""
Простой калькулятор с CLI интерфейсом (argparse)
"""

import argparse
import sys


def add(a: float, b: float) -> float:
    """Сложение двух чисел"""
    return a + b


def subtract(a: float, b: float) -> float:
    """Вычитание двух чисел"""
    return a - b


def multiply(a: float, b: float) -> float:
    """Умножение двух чисел"""
    return a * b


def divide(a: float, b: float) -> float:
    """Деление двух чисел"""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calc",
        description="Простой калькулятор для базовых операций",
        epilog="""
Примеры:
  python calculator.py add 5 3
  python calculator.py multiply 4 2 -v
  python calculator.py divide 10 2
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Выберите операцию",
        required=True,
    )
    
    def add_command_parser(name: str, help_text: str):
        """Создает парсер для команды"""
        cmd_parser = subparsers.add_parser(
            name,
            help=help_text,
        )
        cmd_parser.add_argument(
            "a",
            type=float,
            help="Первое число",
        )
        cmd_parser.add_argument(
            "b",
            type=float,
            help="Второе число",
        )
        return cmd_parser
    
    add_command_parser("add", "Сложение a + b")
    add_command_parser("subtract", "Вычитание a - b")
    add_command_parser("multiply", "Умножение a * b")
    add_command_parser("divide", "Деление a / b")
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Подробный вывод",
    )
    
    return parser


def calculate(args: argparse.Namespace) -> float:
    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }
    
    if args.command not in operations:
        raise ValueError(f"Неизвестная команда: {args.command}")
    
    return operations[args.command](args.a, args.b)


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        result = calculate(args)
        
        if args.verbose:
            operations_symbol = {
                "add": "+",
                "subtract": "-",
                "multiply": "*",
                "divide": "/",
            }
            symbol = operations_symbol.get(args.command, "?")
            print(f"Операция: {args.a} {symbol} {args.b}")
            print(f"Результат: {result}")
        else:
            print(result)
            
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()