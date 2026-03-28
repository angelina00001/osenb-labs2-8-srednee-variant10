import json
import os
from typing import List, Optional
from .models import Calculation, HistoryStats


class CalculatorRepository:
    
    def __init__(self, storage_file: str = "calculations.json"):
        self.storage_file = storage_file
        self._calculations: List[Calculation] = []
        self._next_id = 1
        self._load_data()
    
    def _load_data(self) -> None:
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._calculations = [
                        Calculation.from_dict(item) for item in data.get("calculations", [])
                    ]
                    self._next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, IOError):
                self._calculations = []
                self._next_id = 1
    
    def _save_data(self) -> None:
        try:
            data = {
                "calculations": [calc.to_dict() for calc in self._calculations],
                "next_id": self._next_id,
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Ошибка сохранения данных: {e}")
    
    def save_calculation(self, calculation: Calculation) -> Calculation:
        calculation.id = self._next_id
        self._next_id += 1
        self._calculations.append(calculation)
        self._save_data()
        return calculation
    
    def get_all_calculations(self) -> List[Calculation]:
        return self._calculations.copy()
    
    def get_calculation_by_id(self, calculation_id: int) -> Optional[Calculation]:
        for calc in self._calculations:
            if calc.id == calculation_id:
                return calc
        return None
    
    def get_calculations_by_operation(self, operation: str) -> List[Calculation]:
        return [calc for calc in self._calculations if calc.operation == operation]
    
    def get_history_stats(self) -> HistoryStats:

        if not self._calculations:
            return HistoryStats()

        operation_counts = {}
        total_result = 0.0
        
        for calc in self._calculations:
            operation_counts[calc.operation] = operation_counts.get(calc.operation, 0) + 1
            total_result += calc.result
        
        most_common = max(operation_counts.items(), key=lambda x: x[1])[0] if operation_counts else None
        
        return HistoryStats(
            total_calculations=len(self._calculations),
            most_common_operation=most_common,
            average_result=total_result / len(self._calculations),
            last_calculation=self._calculations[-1] if self._calculations else None,
        )
    
    def clear_history(self) -> None:
        self._calculations = []
        self._next_id = 1
        self._save_data()
