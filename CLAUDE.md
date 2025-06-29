# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Komunikacija / Communication

**NAPOMENA**: Sva komunikacija sa korisnicima ovog projekta treba da bude na srpskom jeziku koristeći latinično pismo.

## Project Overview

This appears to be a new Python project created in PyCharm. The repository currently contains only the basic project structure:

- `.venv/` - Python virtual environment (already created)
- `.idea/` - PyCharm IDE configuration files
- `.git/` - Git repository initialization
- `.claude/` - Claude Code configuration

## Development Environment

This is a Python project using a virtual environment located at `.venv/`. To activate the virtual environment:

```bash
# On Windows
.venv\Scripts\activate

# On Unix/Linux/macOS
source .venv/bin/activate
```

## Project Status

This is a fresh project with no source code, dependencies, or configuration files yet. Common next steps would be:

1. Create a `requirements.txt` or `pyproject.toml` for dependencies
2. Add source code in a `src/` directory or project root
3. Set up testing framework (pytest is common for Python projects)
4. Add a README.md with project description

## Common Commands

Since no project-specific configuration exists yet, standard Python commands would apply:

```bash
# Install dependencies (once requirements.txt exists)
pip install -r requirements.txt

# Run Python files
python <filename>.py

# Install packages
pip install <package_name>

# List installed packages
pip list
```

Note: This CLAUDE.md should be updated as the project structure and tooling are established.