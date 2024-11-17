from setuptools import setup, find_packages

setup(
    name="convert-all",  # Package name
    version="1.0.0",          # Version number
    author="Pavel Polivka",
    author_email="pavel.polivka@hey.com",
    description="A CLI tool to convert files between formats",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PavlikPolivka/convert-anything",
    packages=find_packages(),
    install_requires=[
        "click",
        "ffmpeg-python",
        "Pillow",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "convert=converter.core:convert",
        ],
    },
)
