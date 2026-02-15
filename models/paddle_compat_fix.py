"""
Compatibility fix for PaddleOCR's outdated langchain imports.
This creates a shim to make paddlex work with newer langchain versions.
"""

import sys
from types import ModuleType

# Create fake langchain.docstore module for paddlex compatibility
docstore_module = ModuleType('langchain.docstore')
document_module = ModuleType('langchain.docstore.document')

# Import the actual Document class from its new location
from langchain_community.docstore.document import Document

# Add Document to the fake module
document_module.Document = Document
docstore_module.document = document_module

# Register the fake modules
sys.modules['langchain.docstore'] = docstore_module
sys.modules['langchain.docstore.document'] = document_module

print("✅ PaddleOCR compatibility shim loaded")
