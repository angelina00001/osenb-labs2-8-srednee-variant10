import argparse
import sys
from typing import List
from services.calculator_service import CalculatorService


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calc",
        description="Продвинутый калькулятор с историей вычислений",
        epilog="""
Примеры:
  calc add 5 3           # Сложение
  calc history           # История вычислений
  calc stats             # Статистика
  calc clear             # Очистка истории
  calc get 1             # Получить вычисление по ID
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Команды калькулятора",
        required=True,
    )

    math_parser = argparse.ArgumentParser(add_help=False)
    math_parser.add_argument("a", help="Первое число")
    math_parser.add_argument("b", help="Второе число")

    operations = ["add", "subtract", "multiply", "divide", "power"]
    for op in operations:
        subparsers.add_parser(
            op,
            parents=[math_parser],
            help=f"Операция {op}",
        )
    
    subparsers.add_parser(
        "history",
        help="Показать историю вычислений",
    )

    subparsers.add_parser(
        "stats",
        help="Показать статистику",
    )
  
    subparsers.add_parser(
        "clear",
        help="Очистить историю вычислений",
    )
    
    get_parser = subparsers.add_parser(
        "get",
        help="Получить вычисление по ID",
    )
    get_parser.add_argument("id", type=int, help="ID вычисления")
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Подробный вывод",
    )
    
    return parser


def print_calculation(calc: dict, verbose: bool = False) -> None:
    operations_symbol = {
        "add": "+", "subtract": "-", "multiply": "*",
        "divide": "/", "power": "^",
    }
    
    symbol = operations_symbol.get(calc["operation"], "?")
    
    if verbose:
        print(f"ID: {calc['id']}")
        print(f"Операция: {calc['operand1']} {symbol} {calc['operand2']}")
        print(f"Результат: {calc['result']}")
        print(f"Время: {calc['timestamp']}")
        print("-" * 40)
    else:
        print(f"{calc['operand1']} {symbol} {calc['operand2']} = {calc['result']}")


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    service = CalculatorService()
    
    try:
        if args.command in ["add", "subtract", "multiply", "divide", "power"]:
            a, b = service.validate_input(args.command, args.a, args.b)

            calculation = service.calculate(args.command, a, b)

            if args.verbose:
                print(" Вычисление выполнено и сохранено")
                print_calculation(calculation.to_dict(), verbose=True)
            else:
                print(calculation.result)
        
        elif args.command == "history":
            history = service.get_history()
            if not history:
                print("История вычислений пуста")
            else:
                print(f"История вычислений (всего: {len(history)}):")
                print("=" * 40)
                for calc in history:
                    print_calculation(calc, args.verbose)
        
        elif args.command == "stats":
            stats = service.get_stats()
            print(" Статистика вычислений:")
            print(f"  Всего вычислений: {stats['total_calculations']}")
            print(f"  Самая частая операция: {stats['most_common_operation'] or 'нет'}")
            print(f"  Средний результат: {stats['average_result']}")
            
            if stats['last_calculation']:
                print(f"  Последнее вычисление:")
                print_calculation(stats['last_calculation'], args.verbose)
        
        elif args.command == "clear":
            service.clear_history()
            print("История вычислений очищена")
        
        elif args.command == "get":
            calc = service.get_calculation_by_id(args.id)
            if calc:
                print_calculation(calc, args.verbose)
            else:
                print(f"Вычисление с ID {args.id} не найдено")
        
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
