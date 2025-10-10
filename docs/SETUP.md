# Setup Guide

## Prerequisites

- Python 3.9 or higher
- Git
- A text editor or IDE

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AlenJoseph/ai-prompt-lab.git
cd ai-prompt-lab
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Validate Existing Prompts

```bash
# Validate all prompts
python core/prompt_validator.py prompts/

# Validate specific category
python core/prompt_validator.py prompts/education/

# Validate single file
python core/prompt_validator.py prompts/education/edu_001_explain_simple.json
```

### Using the CLI Tool

```bash
# Create a new prompt interactively
python core/cli.py create

# List all prompts
python core/cli.py list

# List prompts by category
python core/cli.py list -c education

# Show statistics
python core/cli.py stats

# Validate prompts
python core/cli.py validate
python core/cli.py validate prompts/coding/
```

## Development Setup

### Install Development Dependencies

Development dependencies are included in `requirements.txt`. Make sure you've run:

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest tests/test_validator.py
```

### Code Quality

```bash
# Format code with black
black core/ tests/

# Lint code
flake8 core/ tests/

# Type checking
mypy core/
```

## Project Structure

```
ai-prompt-lab/
├── core/                    # Core validation and CLI tools
│   ├── prompt_schema.json   # JSON schema definition
│   ├── prompt_validator.py  # Validation logic
│   └── cli.py              # Command-line interface
├── prompts/                 # Categorized prompts
│   ├── education/
│   ├── creative/
│   ├── productivity/
│   └── coding/
├── docs/                    # Documentation
├── tests/                   # Unit tests
├── .github/workflows/       # CI/CD pipelines
└── requirements.txt         # Python dependencies
```

## Troubleshooting

### Module Not Found Error

If you get `ModuleNotFoundError: No module named 'jsonschema'`:

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Validation Errors

Common validation errors:

1. **Invalid ID format**: Use lowercase letters, numbers, and hyphens only (e.g., `edu-001`)
2. **Score out of range**: Scores must be between 1-5
3. **Missing required field**: Ensure `id`, `title`, `category`, `prompt`, and `responses` are present

### Permission Errors

If you get permission errors when running scripts:

```bash
# Make scripts executable
chmod +x core/cli.py
```

## Next Steps

1. Read the [Prompt Guide](PROMPT_GUIDE.md) to learn how to write effective prompts
2. Read the [Contributing Guide](CONTRIBUTING.md) to learn how to contribute
3. Check out existing prompts in the `prompts/` directory for examples
4. Create your first prompt using `python core/cli.py create`

## Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Start a discussion for questions
- **Documentation**: Check the `/docs` directory

## Resources

- [JSON Schema Documentation](https://json-schema.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
