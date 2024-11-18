# Convert All

`Convert All` is a command-line tool designed to convert files between various formats effortlessly. It's modular and allows developers to extend its functionality by adding new conversion modules.

## Features
- Convert audio files.
- Convert image files.
- Convert video files.
- Modular design for adding custom conversion formats.

---

## Installation

### 1. Clone the Repository
```bash
pip install covert-all
```

---

## Usage

Run the tool with:
```bash
convert-all <input_file> <output_file>
```

Example:
```bash
convert-all input.mp3 output.wav
```

---

## How to Contribute

We welcome contributions to improve the project! Here’s how you can contribute:

### 1. Fork the Repository
Click on the **Fork** button on the top-right corner of the repository page.

### 2. Clone Your Fork
```bash
git clone https://github.com/PavlikPolivka/convert-anything.git branch -M main
cd convert-anything
```

### 3. Add a New Module
1. Navigate to `converter/modules/`.
2. Create a new Python file, e.g., `my_module.py`.
3. Define supported formats and implement the `convert` function:
   ```python
   SUPPORTED_FORMATS = {
       "input": [".source_extension"],
       "output": [".target_extension"]
   }

   def convert(input_file, output_file):
       # Conversion logic here
       pass
   ```

4. Add your module to the repository.


### 5. Submit a Pull Request
Push your changes and open a pull request on the main repository.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
---


Happy converting!
