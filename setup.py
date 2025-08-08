#!/usr/bin/env python3
"""
Setup script for markdown-diagram-fixer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="markdown-diagram-fixer",
    version="1.0.1",
    author="Andrew Yager",
    author_email="andrew@realworldtech.com.au",
    description="A tool to automatically fix formatting and alignment issues in ASCII diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewyager/markdown-diagram-fixer",
    packages=find_packages(),
    py_modules=[
        "precision_diagram_fixer",
        "pandoc_preprocessor"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only standard library
    ],
    entry_points={
        "console_scripts": [
            "diagram-fixer=precision_diagram_fixer:main",
            "pandoc-diagram-fixer=pandoc_preprocessor:main",
            "pandoc-diagram-filter=pandoc_preprocessor:filter_main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["example_diagram.txt", "README.md", "LICENSE"],
    },
    keywords="diagram ascii markdown pandoc formatting alignment",
    project_urls={
        "Bug Reports": "https://github.com/andrewyager/markdown-diagram-fixer/issues",
        "Source": "https://github.com/andrewyager/markdown-diagram-fixer",
        "Documentation": "https://github.com/andrewyager/markdown-diagram-fixer#readme",
    },
)