from typing import Dict, Tuple
from decimal import Decimal, getcontext
from data.models import Calculation
from data.repository import CalculatorRepository


class CalculatorService:
    def __init__(self, repository: CalculatorRepository = None):
        self.repository = repository or CalculatorRepository()
        getcontext().prec = 10
        
        self.operations: Dict[str, Tuple[str, callable]] = {
            "add": ("+", self._add),
            "subtract": ("-", self._subtract),
            "multiply": ("*", self._multiply),
            "divide": ("/", self._divide),
            "power": ("^", self._power),
        }
    
    def _add(self, a: float, b: float) -> float:
        return float(Decimal(str(a)) + Decimal(str(b)))
    
    def _subtract(self, a: float, b: float) -> float:
        return float(Decimal(str(a)) - Decimal(str(b)))
    
    def _multiply(self, a: float, b: float) -> float:
        return float(Decimal(str(a)) * Decimal(str(b)))
    
    def _divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        return float(Decimal(str(a)) / Decimal(str(b)))
    
    def _power(self, a: float, b: float) -> float:
        return a ** b
    
    def calculate(self, operation: str, a: float, b: float) -> Calculation:
        if operation not in self.operations:
            raise ValueError(f"Неподдерживаемая операция: {operation}")
        
        try:
            symbol, func = self.operations[operation]
            result = func(a, b)
            
            calculation = Calculation(
                operation=operation,
                operand1=a,
                operand2=b,
                result=result,
            )
            
            saved_calc = self.repository.save_calculation(calculation)
            return saved_calc
            
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {e}")
    
    def get_history(self) -> list:
        calculations = self.repository.get_all_calculations()
        return [calc.to_dict() for calc in calculations]
    
    def get_stats(self) -> dict:
        stats = self.repository.get_history_stats()
        return {
            "total_calculations": stats.total_calculations,
            "most_common_operation": stats.most_common_operation,
            "average_result": round(stats.average_result, 4) if stats.average_result != 0 else 0,
            "last_calculation": stats.last_calculation.to_dict() if stats.last_calculation else None,
        }
    
    def clear_history(self) -> None:
        self.repository.clear_history()
    
    def get_calculation_by_id(self, calc_id: int) -> dict:
        calc = self.repository.get_calculation_by_id(calc_id)
        return calc.to_dict() if calc else None
    
    def validate_input(self, operation: str, a_str: str, b_str: str) -> Tuple[float, float]:
        if operation not in self.operations:
            raise ValueError(f"Неподдерживаемая операция: {operation}")
        
        try:
            a = float(a_str)
            b = float(b_str)
            return a, b
        except ValueError:
            raise ValueError("Операнды должны быть числами")
