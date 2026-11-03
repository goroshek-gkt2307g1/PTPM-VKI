import sys, os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from Converter import Converter

class TestLab4(unittest.TestCase):
    def test_upper_counts(self):
        self.assertEqual(Converter.do(100.7), 1000)
        self.assertEqual(Converter.do(100.8), 1000)
        self.assertEqual(Converter.do(1e6), 1000)

    def test_positive(self):
        self.assertEqual(Converter.do(0.1), 0)
        self.assertEqual(Converter.do(42.2), 42)
        self.assertEqual(Converter.do(100.6), 100)

    def test_zero(self):
        self.assertRaises(ValueError, Converter.do, 0.0)
        
    def test_negative_mid(self):
        self.assertEqual(Converter.do(-0.1), -5)
        self.assertEqual(Converter.do(-30.4), -35)
        self.assertEqual(Converter.do(-14.1), -19)

    def test_lower_counts(self):
        self.assertEqual(Converter.do(-30.5), -2000)
        self.assertEqual(Converter.do(-90.5), -2000)
        self.assertEqual(Converter.do(-1e6), -2000)

if __name__ == "__main__":
    unittest.main()