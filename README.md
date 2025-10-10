# AI Prompt Lab 🧠

[![Validate Prompts](https://github.com/AlenJoseph/ai-prompt-lab/actions/workflows/validate.yml/badge.svg)](https://github.com/AlenJoseph/ai-prompt-lab/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A community-driven repository for creating, testing, and optimizing prompts across leading AI models (GPT, Gemini, Claude, etc.).

## 🎯 Mission

Build a structured, scalable framework for prompt engineering with **200+ high-performing, well-documented prompts** that anyone can use, test, and improve.

## ✨ Features

- 📋 **Standardized Schema**: All prompts follow a consistent JSON format
- ✅ **Automatic Validation**: Built-in validator ensures quality and consistency
- 🛠️ **CLI Tools**: Easy-to-use commands for creating and managing prompts
- 🔄 **CI/CD Pipeline**: Automated testing and validation on every commit
- 📊 **Multi-Model Support**: Test and compare responses across different AI models
- 📈 **Scoring System**: Evaluate prompts on clarity, accuracy, creativity, and more
- 📚 **Comprehensive Docs**: Guides for contributing, evaluation, and best practices

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AlenJoseph/ai-prompt-lab.git
cd ai-prompt-lab

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Create Your First Prompt

```bash
# Interactive prompt creator
python core/cli.py create

# Or manually create a JSON file following the schema
```

### Validate Prompts

```bash
# Validate all prompts
python core/cli.py validate

# Validate specific category
python core/cli.py validate prompts/education/
```

### Browse Prompts

```bash
# List all prompts
python core/cli.py list

# Filter by category
python core/cli.py list -c coding

# View statistics
python core/cli.py stats
```

## 📁 Repository Structure

```
ai-prompt-lab/
│
├── core/                           # Core tools and utilities
│   ├── prompt_schema.json          # JSON schema definition
│   ├── prompt_validator.py         # Validation engine
│   └── cli.py                      # Command-line interface
│
├── prompts/                        # Categorized prompts
│   ├── education/                  # Learning & teaching prompts
│   ├── creative/                   # Writing & creative prompts
│   ├── productivity/               # Work & efficiency prompts
│   └── coding/                     # Programming prompts
│
├── docs/                           # Documentation
│   ├── SETUP.md                    # Installation guide
│   ├── PROMPT_GUIDE.md             # How to write prompts
│   ├── EVALUATION_GUIDE.md         # Scoring criteria
│   └── CONTRIBUTING.md             # Contribution guidelines
│
├── tests/                          # Unit tests
│   └── test_validator.py
│
├── .github/workflows/              # CI/CD automation
│   └── validate.yml
│
└── requirements.txt                # Python dependencies
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[Prompt Guide](docs/PROMPT_GUIDE.md)** - Writing effective prompts
- **[Evaluation Guide](docs/EVALUATION_GUIDE.md)** - Scoring and testing
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute

## � Prompt Format

All prompts follow this standardized JSON format:

```json
{
  "id": "category-###",
  "title": "Descriptive Title",
  "category": "education|creative|productivity|coding",
  "goal": "What this prompt achieves",
  "prompt": "The actual prompt text with {variables}",
  "variables": ["variable1", "variable2"],
  "tags": ["relevant", "tags"],
  "models_tested": ["gpt-4", "claude-3"],
  "responses": {
    "gpt-4": "Model response here",
    "claude-3": "Model response here"
  },
  "score": {
    "clarity": 5,
    "accuracy": 5,
    "creativity": 4,
    "effectiveness": 5,
    "reusability": 5
  },
  "last_updated": "2025-10-10"
}
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a new prompt following our schema
3. **Validate** using `python core/cli.py validate`
4. **Test** the prompt with AI models
5. **Submit** a pull request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## 📊 Current Stats

- **Total Prompts**: 10+
- **Categories**: 4 (Education, Creative, Productivity, Coding)
- **Models Tested**: GPT-4, Claude-3, Gemini Pro
- **Contributors**: Growing!

## 🎯 Roadmap

### Phase 1: Foundation (Current)
- [x] Core schema and validator
- [x] CLI tools
- [x] CI/CD pipeline
- [x] Initial documentation
- [x] Sample prompts (10+)
- [ ] Reach 50 prompts

### Phase 2: Expansion (Next)
- [ ] Web interface for browsing prompts
- [ ] Advanced analytics and comparison tools
- [ ] Model-specific optimization guides
- [ ] API for programmatic access
- [ ] Reach 200+ prompts

### Phase 3: Community (Future)
- [ ] User ratings and feedback system
- [ ] Prompt versioning and history
- [ ] Integration with popular AI tools
- [ ] Automated prompt testing
- [ ] Community leaderboard

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All contributors who have added prompts and improvements
- The AI community for prompt engineering best practices
- Open source projects that inspired this work

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/AlenJoseph/ai-prompt-lab/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AlenJoseph/ai-prompt-lab/discussions)
- **Email**: alenjoseph333@gmail.com

---

**Star ⭐ this repository if you find it helpful!**

Made with ❤️ by the AI Prompt Lab community
