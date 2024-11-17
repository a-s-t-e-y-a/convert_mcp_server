from setuptools import setup, find_packages

setup(
    name="convert-anything",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "ffmpeg-python",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "convert=converter.core:convert"
        ]
    }
)