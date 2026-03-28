from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Calculation:
    id: Optional[int] = None
    operation: str = ""
    operand1: float = 0.0
    operand2: float = 0.0
    result: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Calculation":
        timestamp = data.get("timestamp")
        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        return cls(
            id=data.get("id"),
            operation=data.get("operation", ""),
            operand1=data.get("operand1", 0.0),
            operand2=data.get("operand2", 0.0),
            result=data.get("result", 0.0),
            timestamp=timestamp,
        )


@dataclass
class HistoryStats:
    total_calculations: int = 0
    most_common_operation: Optional[str] = None
    average_result: float = 0.0
    last_calculation: Optional[Calculation] = None