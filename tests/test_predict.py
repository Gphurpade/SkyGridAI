import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class PredictModuleTests(unittest.TestCase):
    def test_predict_module_imports_without_model_files(self):
        import predict

        self.assertTrue(hasattr(predict, "predict_all"))

    def test_predict_all_raises_helpful_error_when_models_are_missing(self):
        import predict

        with self.assertRaisesRegex(RuntimeError, "trained model files are missing"):
            predict.predict_all(1, 12.0, 74.0, 30.0, 20.0)


if __name__ == "__main__":
    unittest.main()
