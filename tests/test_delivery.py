import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from Delivery import calculate_delivery_cost

class TestDelivery(unittest.TestCase):

    """Границы веса"""
    def test_zero_weight(self):
        result = calculate_delivery_cost(0, 100, "обычный", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_weight_less_01(self):
        result = calculate_delivery_cost(0.05, 100, "хрупкий", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_weight_more_50(self):
        result = calculate_delivery_cost(50.01, 100, "обычный", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_min_weight_norm(self):
        result = calculate_delivery_cost(0.1, 100, "обычный", False)
        self.assertNotEqual(result, (-1, "0000-00-00"))

    def test_max_weight_norm(self):
        result = calculate_delivery_cost(50.0, 100, "обычный", False)
        self.assertNotEqual(result, (-1, "0000-00-00"))

    """"Границы дистанции"""

    def test_zero_distance(self):
        result = calculate_delivery_cost(20, 0, "обычный", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_distance_more_5000(self):
        result = calculate_delivery_cost(20, 5001, "обычный", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_min_distance_norm(self):
        result = calculate_delivery_cost(20, 1, "обычный", False)
        self.assertNotEqual(result, (-1, "0000-00-00"))

    def test_max_distance_norm(self):
        result = calculate_delivery_cost(20, 5000, "обычный", False)
        self.assertNotEqual(result, (-1, "0000-00-00"))

    """"Проверки типа посылки"""

    def test_unknown_type(self):
        result = calculate_delivery_cost(20, 20, "лалала", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_base_type(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный", False)
        self.assertEqual(cost, 700)

    def test_hrupk_type(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий", False)
        self.assertEqual(cost, 1000)

    def test_danger_type(self):
        cost, _ = calculate_delivery_cost(1, 100, "опасный", False)
        self.assertEqual(cost, 1700)

    """"Весовые коэфф"""

    def test_weight_coeff_for_5(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный", False)
        self.assertEqual(cost, 840)

    def test_weight_coeff_for_more_20(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    """"Проверки эскпресса"""

    def test_express_is_more_not_express(self):
        cost1, _ = calculate_delivery_cost(1, 100, "обычный", True)
        cost2, _ = calculate_delivery_cost(1, 100, "обычный", False)
        self.assertGreater(cost1, cost2)

    """"Проверки даты доставки"""

    def test_min_one_day(self):
        _, data = calculate_delivery_cost(1, 100, "обычный", False)
        self.assertEqual(data, "2026-09-04")

    def test_express_short_distance_not_zero_days(self):
        _, data = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertEqual(data, "2026-09-04")

if __name__ == '__main__':
    unittest.main()