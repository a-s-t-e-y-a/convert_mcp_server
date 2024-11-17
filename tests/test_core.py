import unittest
from converter.registry import Registry


class TestCore(unittest.TestCase):
    def test_registry_loads_modules(self):
        registry = Registry()
        self.assertGreater(len(registry.modules), 0, "Modules should be loaded")

    def test_find_valid_module(self):
        registry = Registry()
        module = registry.find_module("input.mp3", "output.wav")
        self.assertIsNotNone(module, "A valid module should be found for MP3 to WAV")


if __name__ == "__main__":
    unittest.main()
