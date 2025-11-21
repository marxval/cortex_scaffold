#!/usr/bin/env python3
"""
Production-grade Python project scaffolding script.
Acts like npm init for Python projects with FastAPI support.
"""

import os
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional


def to_kebab_case(name: str) -> str:
    """Convert project name to kebab-case."""
    # Replace spaces and underscores with hyphens
    name = re.sub(r'[\s_]+', '-', name)
    # Convert to lowercase
    name = name.lower()
    # Remove any non-alphanumeric characters except hyphens
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    return name.strip('-')


def to_snake_case(name: str) -> str:
    """Convert module name to snake_case."""
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[\s-]+', '_', name)
    # Convert to lowercase
    name = name.lower()
    # Remove any non-alphanumeric characters except underscores
    name = re.sub(r'[^a-z0-9_]', '', name)
    # Remove multiple consecutive underscores
    name = re.sub(r'_+', '_', name)
    # Remove leading/trailing underscores
    return name.strip('_')


def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    
    response = input(full_prompt).strip()
    return response if response else (default or "")


def get_yes_no(prompt: str, default: bool = False) -> bool:
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    
    return response in ('y', 'yes')


def create_directory(path: Path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str):
    """Write content to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def write_binary_file(path: Path, content: bytes):
    """Write binary content to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def generate_gitignore(project_name: str) -> str:
    """Generate Python .gitignore content."""
    return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
downloads/*
!downloads/.gitkeep
config/config.py
"""


def generate_mit_license(year: int = None, author: str = "Your Name") -> str:
    """Generate MIT License content."""
    if year is None:
        from datetime import datetime
        year = datetime.now().year
    
    return f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def generate_favicon_ico() -> bytes:
    """
    Generate a simple favicon.ico file.
    
    Creates a minimal valid ICO file with a simple blue square icon.
    
    Returns:
        Bytes representing a valid ICO file
    """
    # ICO file format structure:
    # - ICO header (6 bytes)
    # - Icon directory entry (16 bytes per image)
    # - Image data (BMP format)
    
    # Simple 16x16 icon with blue background
    # This is a minimal valid ICO file with a 16x16x32bpp image
    
    width = 16
    height = 16
    bpp = 32  # bits per pixel
    
    # Calculate sizes
    pixel_data_size = width * height * (bpp // 8)  # 16 * 16 * 4 = 1024 bytes
    bmp_header_size = 40
    total_image_size = bmp_header_size + pixel_data_size
    
    # ICO Header (6 bytes)
    ico_data = bytearray()
    ico_data.extend(b'\x00\x00')  # Reserved (must be 0)
    ico_data.extend(b'\x01\x00')  # Type (1 = ICO)
    ico_data.extend(b'\x01\x00')  # Number of images
    
    # Icon Directory Entry (16 bytes)
    ico_data.extend(bytes([width]))      # Width (16)
    ico_data.extend(bytes([height]))     # Height (16)
    ico_data.extend(b'\x00')             # Color palette (0 = no palette)
    ico_data.extend(b'\x00')             # Reserved
    ico_data.extend(b'\x01\x00')         # Color planes (1)
    ico_data.extend(b'\x20\x00')         # Bits per pixel (32)
    ico_data.extend(total_image_size.to_bytes(4, 'little'))  # Image size
    offset = 6 + 16  # ICO header + directory entry
    ico_data.extend(offset.to_bytes(4, 'little'))  # Offset to image data
    
    # BMP Image Data (embedded in ICO)
    # BMP Header (40 bytes) - Note: height is doubled for ICO format
    bmp_header = bytearray()
    bmp_header.extend(b'\x28\x00\x00\x00')  # Header size (40)
    bmp_header.extend(width.to_bytes(4, 'little'))  # Width (16)
    bmp_header.extend((height * 2).to_bytes(4, 'little'))  # Height (32 = 16*2 for XOR+AND masks)
    bmp_header.extend(b'\x01\x00')          # Color planes (1)
    bmp_header.extend(b'\x20\x00')          # Bits per pixel (32)
    bmp_header.extend(b'\x00\x00\x00\x00')  # Compression (0 = none)
    bmp_header.extend(pixel_data_size.to_bytes(4, 'little'))  # Image size (1024 bytes)
    bmp_header.extend(b'\x00\x00\x00\x00')  # X pixels per meter
    bmp_header.extend(b'\x00\x00\x00\x00')  # Y pixels per meter
    bmp_header.extend(b'\x00\x00\x00\x00')  # Colors used
    bmp_header.extend(b'\x00\x00\x00\x00')  # Important colors
    
    # Pixel data: 16x16 pixels, 32 bits per pixel (BGRA format, bottom-up)
    # Create a simple blue square with a subtle gradient
    pixels = bytearray()
    for y in range(height - 1, -1, -1):  # Bottom-up order for BMP
        for x in range(width):
            # Simple blue color with slight variation
            blue = 100 + (x * 3) % 50
            green = 50 + (y * 2) % 30
            red = 30
            alpha = 255
            
            pixels.extend(bytes([blue, green, red, alpha]))  # BGRA format
    
    # AND mask (1 bit per pixel, all zeros for transparency via alpha channel)
    and_mask_size = (width * height + 7) // 8  # 1 bit per pixel, rounded up
    and_mask = bytearray(and_mask_size)  # All zeros
    
    # Combine all parts
    ico_data.extend(bmp_header)
    ico_data.extend(pixels)
    ico_data.extend(and_mask)
    
    return bytes(ico_data)


def generate_logging_utils() -> str:
    """Generate logging utility module."""
    return '''"""Logging utilities for the project."""
import logging
import sys
from typing import Optional

_loggers: dict[str, logging.Logger] = {}
_handler_attached = False


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with consistent formatting.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    global _handler_attached
    
    if name in _loggers:
        return _loggers[name]
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Only attach handler once to root logger
    if not _handler_attached:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
        _handler_attached = True
    
    _loggers[name] = logger
    return logger
'''


def generate_config_py(project_name: str) -> str:
    """Generate config.py file."""
    return f'''"""Configuration module for {project_name}."""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Environment
ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
'''


def generate_config_example_py() -> str:
    """Generate config_example.py file."""
    return '''"""Example configuration file.

Copy this file to config.py and update with your actual values.
Do not commit config.py to version control.
"""

# Environment
ENV = "development"  # development, staging, production
DEBUG = True

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# Logging
LOG_LEVEL = "INFO"
'''


def generate_module_py(module_name: str, package_name: str) -> str:
    """Generate a module file."""
    snake_module = to_snake_case(module_name)
    return f'''"""Module: {module_name}"""
from {package_name}.utils.logging import get_logger

logger = get_logger(__name__)


def init_module():
    """Initial hook for module {module_name}."""
    logger.info("Initializing {module_name} module...")


def ping():
    """Health check endpoint for {module_name} module."""
    return {{"module": "{snake_module}", "status": "ok"}}
'''


def generate_main_py(project_name: str, package_name: str, modules: List[str]) -> str:
    """Generate main.py with FastAPI app."""
    module_imports = []
    init_calls = []
    ping_routes = []
    module_list = []
    
    for module in modules:
        snake_module = to_snake_case(module)
        module_imports.append(f"from {package_name}.{snake_module} import init_module as {snake_module}_init, ping as {snake_module}_ping")
        init_calls.append(f"    {snake_module}_init()")
        ping_routes.append(f'''@app.get("/{snake_module}/ping")
async def {snake_module}_ping_route():
    """Health check endpoint for {module} module."""
    return {snake_module}_ping()''')
        module_list.append(f'        "{snake_module}",')
    
    imports = "\n".join(module_imports)
    inits = "\n".join(init_calls)
    routes = "\n\n".join(ping_routes)
    module_list_str = "\n".join(module_list)
    
    return f'''"""Main FastAPI application for {project_name}."""
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
{imports}


def init_all_modules():
    """Initialize all registered modules."""
{inits}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    init_all_modules()
    yield
    # Shutdown (if needed, add cleanup code here)


app = FastAPI(
    title="{project_name}",
    description="A FastAPI application",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
async def index():
    """Index route listing all available modules."""
    return JSONResponse(content={{
        "project": "{project_name}",
        "modules": [
{module_list_str}
        ]
    }})


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve favicon."""
    favicon_path = Path(__file__).parent / "favicon.ico"
    return FileResponse(favicon_path)


{routes}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''


def generate_readme(project_name: str, description: str, modules: List[str]) -> str:
    """Generate README.md."""
    module_list = "\n".join([f"- `{to_snake_case(m)}`" for m in modules])
    
    return f'''# {project_name}

{description}

## Project Structure

```
{project_name}/
├── config/          # Configuration files
├── docs/            # Documentation
├── downloads/       # Download directory
├── test/           # Test files
└── {to_snake_case(project_name)}/  # Main package
    ├── utils/      # Utility modules
    └── modules/    # Feature modules
```

## Modules

{module_list}

## Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy configuration:
```bash
cp config/config_example.py config/config.py
```

4. Run the application:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `GET /` - List all modules
- `GET /{{module}}/ping` - Health check for each module

## Development

Run tests:
```bash
pytest test/
```

## License

MIT License - see LICENSE file for details.
'''


def generate_note_for_agents(project_name: str, description: str, modules: List[str]) -> str:
    """Generate NOTE_FOR_AGENTS.md."""
    module_list = "\n".join([f"- `{to_snake_case(m)}`" for m in modules])
    
    return f'''# Note for AI Agents

This is a Python FastAPI project: **{project_name}**

## Description
{description}

## Architecture

This project follows a modular architecture with the following structure:

- Main package: `{to_snake_case(project_name)}/`
- Modules: {len(modules)} module(s)
- Framework: FastAPI
- Python version: 3.10+

## Modules

{module_list}

## Key Files

- `main.py` - FastAPI application entry point
- `config/config.py` - Configuration (not in git)
- `config/config_example.py` - Example configuration
- `{to_snake_case(project_name)}/utils/logging.py` - Logging utilities

## Module Pattern

Each module follows this pattern:
- Located in `{to_snake_case(project_name)}/{{module}}.py`
- Contains `init_module()` function called on startup
- Contains `ping()` function for health checks
- Has a `/{{module}}/ping` route in FastAPI

## Testing

Tests are located in `test/` directory following the pattern `test_{{module}}.py`.

## Development Guidelines

- Use the logging utility: `from {to_snake_case(project_name)}.utils.logging import get_logger`
- Follow the module pattern for new features
- Update documentation in `docs/` directory
- Write tests for new modules
'''


def generate_module_docs_readme(module_name: str) -> str:
    """Generate module documentation README."""
    return f'''# {module_name} Module

## Overview

This module provides functionality for {module_name}.

## Usage

```python
from {to_snake_case(module_name)} import init_module, ping

# Initialize the module
init_module()

# Check health
status = ping()
```

## API Endpoints

- `GET /{to_snake_case(module_name)}/ping` - Health check endpoint

## Configuration

Module-specific configuration can be added to `config/config.py`.
'''


def generate_test_module(module_name: str, package_name: str) -> str:
    """Generate test file for a module."""
    snake_module = to_snake_case(module_name)
    
    return f'''"""Tests for {module_name} module."""
import pytest
from {package_name}.{snake_module} import init_module, ping


def test_init_module():
    """Test module initialization."""
    init_module()
    # Add assertions as needed


def test_ping():
    """Test ping endpoint."""
    result = ping()
    assert result["module"] == "{snake_module}"
    assert result["status"] == "ok"
'''


def generate_test_readme() -> str:
    """Generate test README."""
    return '''# Tests

This directory contains test files for the project.

## Running Tests

```bash
pytest test/
```

## Test Structure

- `test_*.py` - Test files for each module
- `docs/` - Test documentation
'''


def generate_docs_readme(project_name: str) -> str:
    """Generate docs README."""
    return f'''# Documentation

Documentation for {project_name}.

## Structure

Each module has its own documentation directory under `docs/<module>/`.
'''


def generate_requirements_txt() -> str:
    """Generate requirements.txt content."""
    return "fastapi\nuvicorn[standard]\n"


def generate_package_init(package_name: str) -> str:
    """Generate package __init__.py."""
    return f'''"""Main package for {package_name}."""
__version__ = "0.1.0"
'''


def generate_utils_init() -> str:
    """Generate utils __init__.py."""
    return '''"""Utility modules."""
from .logging import get_logger

__all__ = ["get_logger"]
'''


def create_github_repo(name: str, description: str, private: bool, token: str) -> Optional[str]:
    """Create a GitHub repository using the API."""
    import urllib.request
    import urllib.error
    
    url = "https://api.github.com/user/repos"
    data = {
        "name": name,
        "description": description,
        "private": private,
        "auto_init": False
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("clone_url") or result.get("ssh_url")
    except urllib.error.HTTPError as e:
        print(f"Warning: Failed to create GitHub repository: {e}")
        return None
    except Exception as e:
        print(f"Warning: Error creating GitHub repository: {e}")
        return None


def validate_structure(project_path: Path, project_name: str, package_name: str, modules: List[str]) -> bool:
    """Validate that all expected files exist."""
    errors = []
    
    # Required files
    required_files = [
        "README.md",
        "LICENSE",
        ".gitignore",
        "main.py",
        "requirements.txt",
        "NOTE_FOR_AGENTS.md",
        "favicon.ico",
        f"{package_name}/__init__.py",
        f"{package_name}/utils/__init__.py",
        f"{package_name}/utils/logging.py",
        "config/config.py",
        "config/config_example.py",
        "docs/README.md",
        "test/README.md",
    ]
    
    # Module files
    for module in modules:
        snake_module = to_snake_case(module)
        required_files.extend([
            f"{package_name}/{snake_module}.py",
            f"docs/{snake_module}/README.md",
            f"test/test_{snake_module}.py",
        ])
    
    for file_path in required_files:
        full_path = project_path / file_path
        if not full_path.exists():
            errors.append(f"Missing: {file_path}")
    
    # Required directories
    required_dirs = [
        "config",
        "docs",
        "downloads",
        "test",
        "test/docs",
        package_name,
        f"{package_name}/utils",
    ]
    
    for module in modules:
        required_dirs.append(f"docs/{to_snake_case(module)}")
    
    for dir_path in required_dirs:
        full_path = project_path / dir_path
        if not full_path.is_dir():
            errors.append(f"Missing directory: {dir_path}")
    
    if errors:
        print("\n❌ Validation errors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("\n✅ Project structure validated successfully!")
    return True


def validate_module_name(module_name: str) -> tuple[bool, Optional[str]]:
    """
    Validate a module name.
    
    Args:
        module_name: The module name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import keyword
    
    if not module_name or not module_name.strip():
        return False, "Module name cannot be empty"
    
    # Convert to snake_case for validation
    snake_name = to_snake_case(module_name)
    
    if not snake_name:
        return False, f"Module name '{module_name}' becomes empty after processing"
    
    # Check length
    if len(snake_name) > 50:
        return False, f"Module name '{module_name}' is too long (max 50 characters)"
    
    if len(snake_name) < 1:
        return False, f"Module name '{module_name}' is too short"
    
    # Check if it's a valid Python identifier
    if not snake_name.isidentifier():
        return False, f"Module name '{module_name}' is not a valid Python identifier (after conversion: '{snake_name}')"
    
    # Check if it's a Python keyword
    if keyword.iskeyword(snake_name):
        return False, f"Module name '{module_name}' is a Python keyword (after conversion: '{snake_name}')"
    
    # Check for reserved names that might cause issues
    reserved_names = {
        'import', 'from', 'as', 'if', 'else', 'elif', 'for', 'while',
        'def', 'class', 'return', 'pass', 'break', 'continue', 'try',
        'except', 'finally', 'raise', 'assert', 'with', 'lambda',
        'yield', 'del', 'global', 'nonlocal', 'in', 'is', 'not', 'and', 'or',
        'None', 'True', 'False', 'print', 'input', 'open', 'file',
        'main', 'init', 'utils', 'config', 'test', 'docs'
    }
    
    if snake_name.lower() in reserved_names:
        return False, f"Module name '{module_name}' conflicts with reserved name (after conversion: '{snake_name}')"
    
    # Check if it starts with a number (after conversion)
    if snake_name and snake_name[0].isdigit():
        return False, f"Module name '{module_name}' cannot start with a number (after conversion: '{snake_name}')"
    
    return True, None


def validate_modules(modules: List[str]) -> tuple[bool, List[str]]:
    """
    Validate a list of module names.
    
    Args:
        modules: List of module names to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    seen_names = set()
    
    for module in modules:
        is_valid, error = validate_module_name(module)
        if not is_valid:
            errors.append(f"'{module}': {error}")
        else:
            snake_name = to_snake_case(module)
            if snake_name in seen_names:
                errors.append(f"'{module}': Duplicate module name (converts to '{snake_name}')")
            else:
                seen_names.add(snake_name)
    
    return len(errors) == 0, errors


def validate_project_name(project_name: str, check_exists: bool = True) -> tuple[bool, Optional[str]]:
    """
    Validate a project name.
    
    Args:
        project_name: The project name to validate
        check_exists: Whether to check if directory already exists
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not project_name or not project_name.strip():
        return False, "Project name cannot be empty"
    
    # Convert to kebab-case for directory name validation
    kebab_name = to_kebab_case(project_name)
    
    if not kebab_name:
        return False, "Project name becomes empty after processing"
    
    # Check length
    if len(kebab_name) > 50:
        return False, "Project name is too long (max 50 characters)"
    
    if len(kebab_name) < 1:
        return False, "Project name is too short"
    
    # Check for invalid characters in directory name
    if not re.match(r'^[a-z0-9-]+$', kebab_name):
        return False, f"Project name contains invalid characters (after conversion: '{kebab_name}')"
    
    # Check if it starts or ends with a hyphen
    if kebab_name.startswith('-') or kebab_name.endswith('-'):
        return False, "Project name cannot start or end with a hyphen"
    
    # Check for reserved directory names
    reserved_dirs = {'.', '..', '.git', '.venv', 'venv', 'env', 'node_modules'}
    if kebab_name.lower() in reserved_dirs:
        return False, f"Project name '{project_name}' conflicts with reserved directory name"
    
    # Check if directory already exists
    if check_exists:
        project_path = Path.cwd() / kebab_name
        if project_path.exists():
            return False, f"Directory '{kebab_name}' already exists in current directory"
    
    return True, None


def extract_project_info_from_ideas(user_input_path: str) -> tuple[Optional[str], List[str], Optional[str]]:
    """Extract project name, modules, and description from ideas file using OpenAI."""
    try:
        import openai
    except ImportError:
        print("❌ OpenAI library not installed. Install with: pip install openai")
        return None, [], None

    # Read user input file
    try:
        with open(user_input_path, 'r', encoding='utf-8') as f:
            user_content = f.read().strip()
    except Exception as e:
        print(f"❌ Error reading ideas file: {e}")
        return None, [], None

    if not user_content:
        print("⚠️  Ideas file is empty")
        return None, [], None

    # Get OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return None, [], None

    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""Analyze the following project ideas and extract:
1. A suitable project name (kebab-case, concise, descriptive)
2. A comma-separated list of module names (snake_case, 3-8 modules for FastAPI routers)
3. A short project description (one sentence, professional)

Ideas:
{user_content}

Guidelines:
- Project name: kebab-case, 2-4 words, descriptive of the main purpose
- Modules: Focus on functional areas (auth, users, database, notifications, etc.), snake_case, 3-8 modules
  IMPORTANT: Do NOT include "api" as a module - the API lives at the root level (main.py) and is not a module
- Description: One clear sentence explaining what the project does

Return your response in this exact JSON format:
{{
  "project_name": "example-project-name",
  "modules": "module1,module2,module3",
  "description": "A concise description of what this project does"
}}"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts project information from requirements. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result_text = response.choices[0].message.content.strip()
        result = json.loads(result_text)

        project_name = result.get("project_name", "").strip()
        modules_text = result.get("modules", "").strip()
        description = result.get("description", "").strip()

        # Parse modules
        modules = [m.strip() for m in modules_text.split(',') if m.strip()]

        # Validate extracted modules
        valid_modules = []
        for module in modules:
            is_valid, error = validate_module_name(module)
            if is_valid:
                valid_modules.append(module)
            else:
                print(f"⚠️  Skipping invalid module '{module}': {error}")

        print(f"✅ Extracted from ideas:")
        print(f"   Project name: {project_name}")
        print(f"   Modules: {', '.join(valid_modules)}")
        print(f"   Description: {description}")

        return project_name if project_name else None, valid_modules, description if description else None

    except json.JSONDecodeError as e:
        print(f"❌ Error parsing OpenAI response: {e}")
        return None, [], None
    except Exception as e:
        print(f"❌ Error extracting project info: {e}")
        return None, [], None


def extract_modules_from_ideas(user_input_path: str) -> List[str]:
    """Extract potential module names from ideas file using OpenAI."""
    try:
        import openai
    except ImportError:
        print("❌ OpenAI library not installed. Install with: pip install openai")
        return []

    # Read user input file
    try:
        with open(user_input_path, 'r', encoding='utf-8') as f:
            user_content = f.read().strip()
    except Exception as e:
        print(f"❌ Error reading ideas file: {e}")
        return []

    if not user_content:
        print("⚠️  Ideas file is empty")
        return []

    # Get OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return []

    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""Analyze the following project ideas and extract a list of potential module names for a FastAPI application.

Ideas:
{user_content}

Please extract module names that would be suitable for a deep module that will expose functionality through a FastAPI router. Return them as a comma-separated list.

Guidelines:
- Focus on functional areas (auth, users, database, notifications, etc.)
- Use snake_case naming
- Keep names concise but descriptive
- Extract 3-8 modules maximum
- Only include modules that make sense for a web API
- IMPORTANT: Do NOT include "api" as a module - the API lives at the root level (main.py) and is not a module

Examples of good modules: auth, users, database, notifications, payments, analytics

Return only the comma-separated list, no explanation."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts module names from project requirements."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3
        )

        modules_text = response.choices[0].message.content.strip()
        modules = [m.strip() for m in modules_text.split(',') if m.strip()]

        # Validate extracted modules
        valid_modules = []
        for module in modules:
            is_valid, error = validate_module_name(module)
            if is_valid:
                valid_modules.append(module)
            else:
                print(f"⚠️  Skipping invalid module '{module}': {error}")

        print(f"✅ Extracted {len(valid_modules)} modules from ideas: {', '.join(valid_modules)}")
        return valid_modules

    except Exception as e:
        print(f"❌ Error extracting modules: {e}")
        return []


def enhance_readme_with_openai(base_readme: str, user_input_path: str, project_name: str, description: str, modules: List[str]) -> str:
    """Enhance README using OpenAI API based on user input."""
    try:
        import openai
    except ImportError:
        print("❌ OpenAI library not installed. Install with: pip install openai")
        return base_readme

    # Read user input file
    try:
        with open(user_input_path, 'r', encoding='utf-8') as f:
            user_content = f.read().strip()
    except FileNotFoundError:
        print(f"❌ User input file not found: {user_input_path}")
        return base_readme
    except Exception as e:
        print(f"❌ Error reading user input file: {e}")
        return base_readme

    if not user_content:
        print("⚠️  User input file is empty, using standard README")
        return base_readme

    # Get OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return base_readme

    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""You are a technical writer enhancing a README.md file for a Python FastAPI project.

Project Information:
- Project Name: {project_name}
- Description: {description}
- Modules: {', '.join(modules)}

Current README structure:
{base_readme}

User's additional ideas and requirements:
{user_content}

Please enhance the README by:
1. Incorporating the user's ideas and requirements into the existing structure
2. Maintaining the professional format and structure
3. Adding any relevant sections that would be helpful based on the user's input
4. Ensuring all sections remain practical and actionable
5. Keeping the README comprehensive but not overwhelming

Return the complete enhanced README.md content, maintaining markdown formatting."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful technical writer who enhances README files by incorporating user requirements while maintaining professional standards."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        enhanced_readme = response.choices[0].message.content.strip()

        # Ensure it starts with proper markdown headers
        if not enhanced_readme.startswith('# '):
            enhanced_readme = f"# {project_name}\n\n{enhanced_readme}"

        print("✅ README enhanced with OpenAI")
        return enhanced_readme

    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}")
        return base_readme


def main():
    """Main scaffolding function."""
    parser = argparse.ArgumentParser(
        description="Python Project Scaffolder - Create FastAPI projects with modular architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cortex_scaffold.py                           # Interactive mode (with defaults)
  python cortex_scaffold.py --help                    # Show this help
  python cortex_scaffold.py --inspire ideas.txt       # AI extracts project name, modules, and description from ideas

Interactive Mode Defaults (without --inspire):
  Project name: my_fastapi_project
  Modules: users,auth
  Description: A micromodular project powered by CortexScaffold and FastAPI

With --inspire flag:
  AI automatically extracts project name, modules, and description from your ideas file.
  You can just hit Enter to accept all AI-generated defaults!

Setup OpenAI API key:
  export OPENAI_API_KEY="your-api-key-here"
        """
    )

    parser.add_argument(
        "--inspire",
        type=str,
        help="Path to a .txt file containing ideas to enhance the README using OpenAI API. Requires OPENAI_API_KEY environment variable."
    )

    args = parser.parse_args()

    # Validate inspire file if provided
    if args.inspire:
        if not args.inspire.endswith('.txt'):
            print("❌ Error: Inspiration file must be a .txt file")
            sys.exit(1)
        if not os.path.exists(args.inspire):
            print(f"❌ Error: Inspiration file not found: {args.inspire}")
            sys.exit(1)

    print("=" * 60)
    print("Python Project Scaffolder")
    print("=" * 60)
    print()

    # Extract project info from ideas file if --inspire is used
    default_project_name = "my_fastapi_project"
    default_modules = "users,auth"
    default_description = "A micromodular project powered by CortexScaffold and FastAPI"

    if args.inspire:
        print("🤖 Extracting project information from ideas file...")
        extracted_name, extracted_modules, extracted_description = extract_project_info_from_ideas(args.inspire)
        
        if extracted_name:
            default_project_name = extracted_name
        if extracted_modules:
            default_modules = ",".join(extracted_modules)
        if extracted_description:
            default_description = extracted_description
        print()

    # Get project information
    project_name = get_user_input("Project name", default_project_name)
    if not project_name:
        print("Error: Project name is required.")
        sys.exit(1)

    # Validate project name
    is_valid, error = validate_project_name(project_name)
    if not is_valid:
        print(f"\n❌ Project name validation error: {error}")
        sys.exit(1)

    # Get modules
    modules_input = get_user_input("Modules (comma-separated)", default_modules)
    if not modules_input:
        print("Error: At least one module is required.")
        sys.exit(1)
    modules = [m.strip() for m in modules_input.split(",") if m.strip()]

    if not modules:
        print("Error: At least one module is required.")
        sys.exit(1)

    # Validate module names
    is_valid, validation_errors = validate_modules(modules)
    if not is_valid:
        print("\n❌ Module name validation errors:")
        for error in validation_errors:
            print(f"  - {error}")
        print("\nPlease use valid Python module names (will be converted to snake_case).")
        print("Module names cannot be Python keywords or reserved names.")
        sys.exit(1)

    description = get_user_input("Short description", default_description)

    init_git = get_yes_no("Initialize git repository?", True)

    github_private = False
    create_github = False
    if init_git:
        create_github = get_yes_no("Create GitHub repository?", False)
        if create_github:
            github_private = not get_yes_no("Make repository public?", True)
    
    # Generate names
    kebab_name = to_kebab_case(project_name)
    snake_package = to_snake_case(project_name)
    
    # Create project directory
    project_path = Path.cwd() / kebab_name
    
    # Note: Directory existence is already validated earlier, but double-check here
    # in case something changed between validation and creation
    if project_path.exists():
        print(f"\n❌ Error: Directory '{kebab_name}' already exists in current directory.")
        print("   Please choose a different project name or remove the existing directory.")
        sys.exit(1)
    
    print(f"\n📁 Creating project structure in '{kebab_name}'...")
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    create_directory(project_path / "config")
    create_directory(project_path / "docs")
    create_directory(project_path / "downloads")
    create_directory(project_path / "test")
    create_directory(project_path / "test" / "docs")
    create_directory(project_path / snake_package)
    create_directory(project_path / snake_package / "utils")
    
    for module in modules:
        create_directory(project_path / "docs" / to_snake_case(module))
    
    # Create root files
    print("📝 Generating files...")

    # Generate base README
    base_readme = generate_readme(project_name, description, modules)

    # Enhance README with OpenAI if requested
    if args.inspire:
        enhanced_readme = enhance_readme_with_openai(base_readme, args.inspire, project_name, description, modules)
        write_file(project_path / "README.md", enhanced_readme)
    else:
        write_file(project_path / "README.md", base_readme)

    write_file(project_path / "NOTE_FOR_AGENTS.md", generate_note_for_agents(project_name, description, modules))
    write_file(project_path / "LICENSE", generate_mit_license())
    write_file(project_path / ".gitignore", generate_gitignore(project_name))
    write_file(project_path / "requirements.txt", generate_requirements_txt())
    write_binary_file(project_path / "favicon.ico", generate_favicon_ico())
    
    # Create main.py
    write_file(project_path / "main.py", generate_main_py(project_name, snake_package, modules))
    
    # Create config files
    write_file(project_path / "config" / "config.py", generate_config_py(project_name))
    write_file(project_path / "config" / "config_example.py", generate_config_example_py())
    
    # Create package files
    write_file(project_path / snake_package / "__init__.py", generate_package_init(snake_package))
    write_file(project_path / snake_package / "utils" / "__init__.py", generate_utils_init())
    write_file(project_path / snake_package / "utils" / "logging.py", generate_logging_utils())
    
    # Create module files
    for module in modules:
        snake_module = to_snake_case(module)
        write_file(
            project_path / snake_package / f"{snake_module}.py",
            generate_module_py(module, snake_package)
        )
        write_file(
            project_path / "docs" / snake_module / "README.md",
            generate_module_docs_readme(module)
        )
        write_file(
            project_path / "test" / f"test_{snake_module}.py",
            generate_test_module(module, snake_package)
        )
    
    # Create documentation files
    write_file(project_path / "docs" / "README.md", generate_docs_readme(project_name))
    write_file(project_path / "test" / "README.md", generate_test_readme())
    
    # Create .gitkeep for downloads
    write_file(project_path / "downloads" / ".gitkeep", "")
    
    # Create virtual environment
    print("🐍 Creating virtual environment...")
    venv_path = project_path / ".venv"
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_path)],
            check=True,
            capture_output=True
        )
        print("✅ Virtual environment created")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to create virtual environment: {e}")
    
    # Initialize git repository
    github_url = None
    if init_git:
        print("🔧 Initializing git repository...")
        try:
            subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=project_path, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=project_path,
                check=True,
                capture_output=True
            )
            print("✅ Git repository initialized")
            
            # Create GitHub repository if requested
            if create_github:
                github_token = os.getenv("GITHUB_TOKEN")
                if github_token:
                    print("🌐 Creating GitHub repository...")
                    github_url = create_github_repo(kebab_name, description, github_private, github_token)
                    if github_url:
                        print(f"✅ GitHub repository created: {github_url}")
                        # Set remote origin
                        try:
                            subprocess.run(
                                ["git", "remote", "add", "origin", github_url],
                                cwd=project_path,
                                check=True,
                                capture_output=True
                            )
                            print("✅ Remote origin set")
                        except subprocess.CalledProcessError:
                            print("⚠️  Warning: Failed to set remote origin")
                    else:
                        print("⚠️  Warning: Failed to create GitHub repository")
                else:
                    print("⚠️  Warning: GITHUB_TOKEN not found in environment")
                    print("   Set GITHUB_TOKEN environment variable to enable GitHub integration")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Git operations failed: {e}")
        except FileNotFoundError:
            print("⚠️  Warning: Git not found. Skipping git initialization.")
    
    # Validate structure
    print("\n🔍 Validating project structure...")
    validate_structure(project_path, project_name, snake_package, modules)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Project scaffolded successfully!")
    print("=" * 60)
    print(f"\nProject location: {project_path.absolute()}")
    print(f"\nNext steps:")
    print(f"  1. cd {kebab_name}")
    print(f"  2. source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
    print(f"  3. pip install -r requirements.txt")
    print(f"  4. python main.py")
    if github_url:
        print(f"\nGitHub repository: {github_url}")
    print()


if __name__ == "__main__":
    main()

