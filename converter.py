import sys
import json
import importlib

def load_settings():
    with open('settings.json', 'r') as f:
        return json.load(f)

def main():
    if len(sys.argv) != 3:
        print("Usage: convert <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    input_ext = input_file.split('.')[-1]
    output_ext = output_file.split('.')[-1]

    settings = load_settings()
    for conversion in settings['conversions']:
        if conversion['input'] == input_ext and conversion['output'] == output_ext:
            module = importlib.import_module(f"converters.{conversion['module']}")
            module.convert(input_file, output_file)
            print(f"Converted {input_file} to {output_file}")
            return

    print(f"No conversion module found for {input_ext} to {output_ext}")
    sys.exit(1)

if __name__ == "__main__":
    main()