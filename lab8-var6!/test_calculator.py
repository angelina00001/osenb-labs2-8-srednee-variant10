import unittest
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from calculator import (
    add,
    subtract,
    multiply,
    divide,
    calculate,
    create_parser,
    main,
)


class TestMathFunctions(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(2.5, 3.5), 6.0)
    
    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)
        self.assertEqual(subtract(0, 0), 0)
        self.assertEqual(subtract(2.5, 1.5), 1.0)
    
    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 5), 0)
        self.assertEqual(multiply(2.5, 2), 5.0)
    
    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(5, 2), 2.5)
        self.assertEqual(divide(0, 5), 0)
        self.assertEqual(divide(-6, 3), -2)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            divide(5, 0)
        self.assertEqual(str(context.exception), "Деление на ноль невозможно")

def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = [
        TestMathFunctions,
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":    
    result = run_all_tests()