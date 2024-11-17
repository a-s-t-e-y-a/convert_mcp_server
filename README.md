
# Convert Anything

`Convert Anything` is a command-line tool designed to convert files between various formats effortlessly. It's modular and allows developers to extend its functionality by adding new conversion modules.

## Features
- Convert audio files (e.g., MP3 to WAV).
- Convert image files (e.g., PNG to JPG).
- Convert video files (e.g., MP4 to AVI).
- Modular design for adding custom conversion formats.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/convert-anything.git
cd convert-anything
```

### 2. Set Up the Environment
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

Run the tool with:
```bash
python -m converter.core <input_file> <output_file>
```

Example:
```bash
python -m converter.core input.mp3 output.wav
```

---

## How to Contribute

We welcome contributions to improve the project! Here’s how you can contribute:

### 1. Fork the Repository
Click on the **Fork** button on the top-right corner of the repository page.

### 2. Clone Your Fork
```bash
git clone https://github.com/PavlikPolivkagit branch -M main/convert-anything.git
cd convert-anything
```

### 3. Set Up the Environment
Follow the [Installation](#installation) instructions to set up your development environment.

### 4. Add a New Module
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

### 5. Test Your Module
Run unit tests:
```bash
pytest
```

### 6. Submit a Pull Request
Push your changes and open a pull request on the main repository.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---


Happy converting!
