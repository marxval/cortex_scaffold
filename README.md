# Cortex Scaffold

A powerful AI-powered Python project scaffolding tool that creates standardized deep module structures. FastAPI is used as a communication tool to expose module functionality, but the core focus is on creating well-structured, deep modules with a consistent directory layout across all projects.

## Features

- 🏗️ Standardized directory structure for consistent project organization
- 📦 Deep module architecture with automatic module generation
- 🤖 AI-powered project setup - extract project name, modules, and description from ideas
- 🎨 AI-enhanced README generation with `--inspire` flag
- 🔌 FastAPI integration for module communication (optional, not the core focus)
- 🐍 Virtual environment setup
- 📝 Comprehensive documentation generation
- 🔧 Git integration with GitHub support

## Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set OpenAI API Key (Optional)

If you want to use the `--inspire` feature for AI-enhanced READMEs and automatic module extraction:

```bash
# For current session
export OPENAI_API_KEY="your-api-key-here"

# Or add to your shell profile for permanent setup
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

### Interactive Mode
```bash
python cortex_scaffold.py
```

The interactive mode provides sensible defaults - just hit Enter to accept them:
- **Project name**: `my_fastapi_project`
- **Modules**: `users,auth` (Note: "api" is not a module - the API lives at root in main.py)
- **Description**: `A deep modular Python project with standardized structure powered by CortexScaffold`

### Command Line Mode
```bash
# Basic scaffolding with defaults
python cortex_scaffold.py

# AI-enhanced README with ideas from file
python cortex_scaffold.py --inspire project_ideas.txt

# Show help
python cortex_scaffold.py --help
```

### The --inspire Feature

When using `--inspire`, the tool will:
1. **Automatically extract** project name, modules, and description from your ideas file using AI
2. Use these as **defaults** in the interactive prompts - just hit Enter to accept them!
3. Enhance the README by combining your standard template with ideas from the file

**Super quick workflow:**
```bash
python cortex_scaffold.py --inspire ideas.txt
# Then just hit Enter 3 times to accept AI-generated:
# - Project name
# - Modules  
# - Description
```

Example ideas file (`project_ideas.txt`):
```
This project should include:
- User authentication with JWT tokens
- Database integration with PostgreSQL
- API endpoints for user management
- Email notifications system
- File upload functionality
- Admin dashboard
- Docker containerization
- CI/CD pipeline setup
```

## Generated Project Structure

The scaffold creates a standardized directory structure that ensures consistency across all projects:

```
your-project/
├── config/              # Configuration files
├── docs/               # Documentation
├── downloads/          # Download directory
├── test/              # Test files
├── your_project/       # Main package with deep modules
│   ├── utils/         # Utility modules
│   └── [modules]/     # Deep feature modules (one per module)
├── main.py            # Application entry point (uses FastAPI for module communication)
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
└── ...
```

Each module is a deep, self-contained structure ready for development, following the standardized layout.

## Requirements

- Python 3.10+
- OpenAI API key (optional, for --inspire feature)

## License

MIT License
