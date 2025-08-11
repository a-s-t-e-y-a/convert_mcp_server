#!/usr/bin/env python3
"""
Test script to verify the API structure
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from converter.registry import Registry
    print("✓ Registry import successful")
    
    registry = Registry()
    print(f"✓ Registry initialized with {len(registry.modules)} modules")
    
    for module in registry.modules:
        module_name = module.__name__.split('.')[-1]
        formats = module.SUPPORTED_FORMATS
        print(f"  - {module_name}: {formats}")
    
    print("\n✓ Converter modules loaded successfully")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

try:
    from fastapi import FastAPI
    print("✓ FastAPI available")
except ImportError:
    print("✗ FastAPI not installed - run: pip install fastapi uvicorn python-multipart")

try:
    import uvicorn
    print("✓ Uvicorn available")
except ImportError:
    print("✗ Uvicorn not installed")

print("\nAPI Structure Test Complete!")
