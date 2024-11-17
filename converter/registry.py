import os
import importlib


class Registry:
    def __init__(self):
        self.modules = []
        self.load_modules()

    def load_modules(self):
        base_path = os.path.dirname(__file__)
        module_path = os.path.join(base_path, "modules")
        for file in os.listdir(module_path):
            if file.endswith(".py") and file != "__init__.py":
                module_name = f"converter.modules.{file[:-3]}"
                module = importlib.import_module(module_name)
                if hasattr(module, "SUPPORTED_FORMATS"):
                    self.modules.append(module)

    def find_module(self, input_file, output_file):
        input_ext = os.path.splitext(input_file)[1].lower()
        output_ext = os.path.splitext(output_file)[1].lower()
        for module in self.modules:
            if input_ext in module.SUPPORTED_FORMATS.get("input", []) and \
                    output_ext in module.SUPPORTED_FORMATS.get("output", []):
                return module
        return None
