# Host Example - Virtual Environment Setup Guide

This guide provides instructions for setting up and managing virtual environments using both UV (modern Python package manager) and native Python venv.

## Prerequisites

- Python 3.13 or higher
- For UV: Install UV package manager

## Method 1: Using UV (Recommended)

UV is a fast Python package manager that provides superior dependency resolution and performance.

### Installing UV

```bash
# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: Using pip
pip install uv
```

### Creating and Using Virtual Environment with UV

```bash
# Navigate to the project directory
cd pico_lora_sx1262/host_example

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate

# Run your Python scripts
python main.py

# Deactivate when done
deactivate
```

### Restoring Environment from Lock File

```bash
# If you have an existing uv.lock file, simply run:
uv sync

# This will recreate the exact environment with pinned dependencies
```

### Adding New Dependencies with UV

```bash
# Add a new dependency
uv add package_name

# Add development dependency
uv add --dev package_name

# Remove a dependency
uv remove package_name
```

## Method 2: Using Native Python venv

### Creating Virtual Environment

```bash
# Navigate to the project directory
cd pico_lora_sx1262/host_example

# Create virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### Installing Dependencies

```bash
# Install dependencies from pyproject.toml
pip install -e .

# Or install specific dependencies manually
pip install pyserial>=3.5

# Create requirements.txt for reproducibility
pip freeze > requirements.txt
```

### Restoring Environment from Requirements

```bash
# If you have a requirements.txt file
pip install -r requirements.txt

# Or reinstall from pyproject.toml
pip install -e .
```

## Managing Dependencies

### Viewing Installed Packages

```bash
# With UV
uv pip list

# With native pip
pip list
```

### Updating Dependencies

```bash
# With UV
uv sync --upgrade

# With native pip
pip install --upgrade package_name
# or
pip install -r requirements.txt --upgrade
```

## Running the Application

Once your virtual environment is activated and dependencies are installed:

```bash
python main.py
```

## Deactivating Virtual Environment

```bash
deactivate
```

## Troubleshooting

### UV Issues
- Ensure UV is properly installed and in your PATH
- Check Python version compatibility (>=3.13 required)
- Try `uv --version` to verify installation

### Native venv Issues
- Ensure Python 3.13+ is installed
- On Windows, you may need to enable script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- If activation fails, check the virtual environment was created successfully

## Project Dependencies

This project requires:
- Python >=3.13
- pyserial >=3.5

For the complete list of dependencies and their versions, refer to `pyproject.toml` and `uv.lock` files.
