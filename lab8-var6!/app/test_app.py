import unittest
import os
import tempfile
import json
from decimal import Decimal

from data.models import Calculation, HistoryStats
from data.repository import CalculatorRepository
from services.calculator_service import CalculatorService


class TestCalculationModel(unittest.TestCase):
    def test_creation_with_defaults(self):
        calc = Calculation()
        
        self.assertEqual(calc.id, None)
        self.assertEqual(calc.operation, "")
        self.assertEqual(calc.operand1, 0.0)
        self.assertEqual(calc.operand2, 0.0)
        self.assertEqual(calc.result, 0.0)
        self.assertIsNotNone(calc.timestamp)
    
    def test_creation_with_values(self):
        calc = Calculation(
            id=1,
            operation="add",
            operand1=5.5,
            operand2=3.2,
            result=8.7,
        )
        
        self.assertEqual(calc.id, 1)
        self.assertEqual(calc.operation, "add")
        self.assertEqual(calc.operand1, 5.5)
        self.assertEqual(calc.operand2, 3.2)
        self.assertEqual(calc.result, 8.7)
    
    def test_to_dict_method(self):
        calc = Calculation(
            id=42,
            operation="multiply",
            operand1=2.5,
            operand2=4.0,
            result=10.0,
        )
        
        result = calc.to_dict()
        
        self.assertEqual(result["id"], 42)
        self.assertEqual(result["operation"], "multiply")
        self.assertEqual(result["operand1"], 2.5)
        self.assertEqual(result["operand2"], 4.0)
        self.assertEqual(result["result"], 10.0)
        self.assertIn("timestamp", result)
    
    def test_from_dict_method(self):
        data = {
            "id": 99,
            "operation": "divide",
            "operand1": 15.0,
            "operand2": 3.0,
            "result": 5.0,
            "timestamp": "2024-01-15T10:30:00",
        }
        
        calc = Calculation.from_dict(data)
        
        self.assertEqual(calc.id, 99)
        self.assertEqual(calc.operation, "divide")
        self.assertEqual(calc.operand1, 15.0)
        self.assertEqual(calc.operand2, 3.0)
        self.assertEqual(calc.result, 5.0)
    
    def test_equality(self):
        calc1 = Calculation(id=1, operation="add", result=5.0)
        calc2 = Calculation(id=1, operation="add", result=5.0)
        calc3 = Calculation(id=2, operation="subtract", result=3.0)

        self.assertNotEqual(calc1, calc2)
        self.assertNotEqual(calc1, calc3)


class TestHistoryStatsModel(unittest.TestCase):
    def test_default_values(self):
        stats = HistoryStats()
        
        self.assertEqual(stats.total_calculations, 0)
        self.assertEqual(stats.most_common_operation, None)
        self.assertEqual(stats.average_result, 0.0)
        self.assertEqual(stats.last_calculation, None)
    
    def test_with_values(self):
        calc = Calculation(operation="add", result=10.0)
        stats = HistoryStats(
            total_calculations=5,
            most_common_operation="multiply",
            average_result=15.5,
            last_calculation=calc,
        )
        
        self.assertEqual(stats.total_calculations, 5)
        self.assertEqual(stats.most_common_operation, "multiply")
        self.assertEqual(stats.average_result, 15.5)
        self.assertEqual(stats.last_calculation, calc)


class TestCalculatorRepository(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix='.json', 
            mode='w'
        )
        self.temp_file.write('{"calculations": [], "next_id": 1}')
        self.temp_file.close()
        self.repository = CalculatorRepository(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_initialization(self):
        self.assertEqual(len(self.repository.get_all_calculations()), 0)
    
    def test_save_calculation_first_time(self):
        calc = Calculation(
            operation="add",
            operand1=2,
            operand2=3,
            result=5,
        )
        
        saved = self.repository.save_calculation(calc)

        self.assertEqual(saved.id, 1)
        self.assertEqual(saved.operation, "add")

        all_calcs = self.repository.get_all_calculations()
        self.assertEqual(len(all_calcs), 1)
        self.assertEqual(all_calcs[0].id, 1)
    
    def test_save_multiple_calculations(self):
        calc1 = Calculation(operation="add", result=5)
        calc2 = Calculation(operation="subtract", result=2)
        
        saved1 = self.repository.save_calculation(calc1)
        saved2 = self.repository.save_calculation(calc2)
        
        self.assertEqual(saved1.id, 1)
        self.assertEqual(saved2.id, 2)
        
        all_calcs = self.repository.get_all_calculations()
        self.assertEqual(len(all_calcs), 2)
    
    def test_get_calculation_by_id_found(self):
        calc = Calculation(operation="add", result=5)
        saved = self.repository.save_calculation(calc)
        
        found = self.repository.get_calculation_by_id(1)
        
        self.assertIsNotNone(found)
        self.assertEqual(found.id, 1)
        self.assertEqual(found.operation, "add")
    
    def test_get_calculation_by_id_not_found(self):
        found = self.repository.get_calculation_by_id(999)
        
        self.assertIsNone(found)
    
    def test_get_calculations_by_operation(self):
        calc1 = Calculation(operation="add", result=5)
        calc2 = Calculation(operation="subtract", result=3)
        calc3 = Calculation(operation="add", result=7)
        
        self.repository.save_calculation(calc1)
        self.repository.save_calculation(calc2)
        self.repository.save_calculation(calc3)
        
        add_calcs = self.repository.get_calculations_by_operation("add")
        subtract_calcs = self.repository.get_calculations_by_operation("subtract")
        multiply_calcs = self.repository.get_calculations_by_operation("multiply")
        
        self.assertEqual(len(add_calcs), 2)
        self.assertEqual(len(subtract_calcs), 1)
        self.assertEqual(len(multiply_calcs), 0)
    
    def test_get_history_stats_empty(self):
        stats = self.repository.get_history_stats()
        
        self.assertEqual(stats.total_calculations, 0)
        self.assertIsNone(stats.most_common_operation)
        self.assertEqual(stats.average_result, 0.0)
        self.assertIsNone(stats.last_calculation)
    
    def test_get_history_stats_with_data(self):
        calc1 = Calculation(operation="add", result=10)
        calc2 = Calculation(operation="add", result=20)
        calc3 = Calculation(operation="multiply", result=30)
        
        self.repository.save_calculation(calc1)
        self.repository.save_calculation(calc2)
        self.repository.save_calculation(calc3)
        
        stats = self.repository.get_history_stats()
        
        self.assertEqual(stats.total_calculations, 3)
        self.assertEqual(stats.most_common_operation, "add")
        self.assertAlmostEqual(stats.average_result, (10 + 20 + 30) / 3)
        self.assertEqual(stats.last_calculation.operation, "multiply")
    
    def test_clear_history(self):
        calc1 = Calculation(operation="add", result=5)
        calc2 = Calculation(operation="subtract", result=3)
        
        self.repository.save_calculation(calc1)
        self.repository.save_calculation(calc2)
        
        self.assertEqual(len(self.repository.get_all_calculations()), 2)
        
        self.repository.clear_history()
        
        self.assertEqual(len(self.repository.get_all_calculations()), 0)

        calc3 = Calculation(operation="multiply", result=10)
        saved = self.repository.save_calculation(calc3)
        self.assertEqual(saved.id, 1)

def create_test_suite():
    test_cases = [
        TestCalculationModel,
        TestHistoryStatsModel,
        TestCalculatorRepository,
    ]
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_case))
    
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    
    result = runner.run(suite)
