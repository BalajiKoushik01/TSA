"""Regression tests: no synthetic accuracy claims and no future leakage."""
import importlib.util
from pathlib import Path
import unittest

module_path = Path(__file__).resolve().parents[1] / "scripts" / "forecast_validation.py"
spec = importlib.util.spec_from_file_location("forecast_validation", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
evaluate = module.rolling_seasonal_naive_rmse


class RealForecastErrorTests(unittest.TestCase):
    def test_exact_repeating_season_has_zero_error(self):
        values = [5.0, 10.0, 15.0] * 10
        sizes, errors = evaluate(values, season_length=3, min_history=6)
        self.assertEqual(sizes[0], 6)
        self.assertEqual(len(errors), 24)
        self.assertTrue(all(value == 0 for value in errors))

    def test_out_of_sample_errors_are_from_observations(self):
        values = [10, 20, 30, 10, 20, 30, 12, 24, 33]
        sizes, errors = evaluate(values, season_length=3, min_history=6)
        self.assertEqual(sizes, [6, 7, 8])
        self.assertAlmostEqual(errors[0], 2)
        self.assertAlmostEqual(errors[1], (10 ** 0.5))
        self.assertAlmostEqual(errors[2], (29 / 3) ** 0.5)

    def test_future_values_do_not_change_prior_predictions(self):
        values = [1, 2, 3] * 10
        old_sizes, old_errors = evaluate(values, season_length=3, min_history=6)
        values[-1] = 500
        new_sizes, new_errors = evaluate(values, season_length=3, min_history=6)
        self.assertEqual(old_sizes, new_sizes)
        self.assertEqual(old_errors[:-1], new_errors[:-1])

    def test_missing_or_nonfinite_values_rejected(self):
        for bad in (float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                evaluate([1, 2, 3, 4, 5, 6, bad], season_length=3, min_history=6)

    def test_short_series_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([1, 2, 3, 4, 5], season_length=3, min_history=6)


if __name__ == "__main__":
    unittest.main()
