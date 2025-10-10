# Contributing to AI Prompt Lab

Thank you for your interest in contributing to the AI Prompt Lab! This document provides guidelines for contributing prompts, improvements, and documentation.

## Table of Contents

1. [Getting Started](#getting-started)
2. [How to Contribute](#how-to-contribute)
3. [Prompt Submission Guidelines](#prompt-submission-guidelines)
4. [Code Contribution Guidelines](#code-contribution-guidelines)
5. [Documentation Guidelines](#documentation-guidelines)
6. [Review Process](#review-process)

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your contribution
4. Make your changes
5. Submit a pull request

## How to Contribute

### Ways to Contribute

- Submit new prompts
- Improve existing prompts
- Add documentation
- Report bugs
- Suggest new features
- Improve code quality

## Prompt Submission Guidelines

### 1. Follow the Schema

All prompts must conform to `core/prompt_schema.json`. Use the validator to check:

```python
from core.prompt_validator import PromptValidator

validator = PromptValidator()
is_valid, error = validator.validate_prompt_file("path/to/your/prompt.json")
```

### 2. Choose the Right Category

Place your prompt in the appropriate category:
- `prompts/education/` - Educational and learning prompts
- `prompts/creative/` - Creative writing and artistic prompts
- `prompts/productivity/` - Workflow and productivity prompts
- `prompts/coding/` - Programming and technical prompts

### 3. Naming Convention

- Use descriptive, kebab-case filenames: `essay-writing-assistant.json`
- Include the category in the filename if helpful: `coding-python-debugger.json`

### 4. Required Fields

Every prompt must include:
- `id`: Unique identifier (format: `category-name-###`)
- `title`: Clear, descriptive title
- `category`: One of the four categories
- `description`: Brief explanation of the prompt's purpose
- `prompt`: The actual prompt text

### 5. Optional but Recommended

- `variables`: Define any placeholders in your prompt
- `tags`: Add relevant tags for discoverability
- `examples`: Provide example inputs and outputs

### 6. Quality Standards

- **Clear**: Easy to understand and follow
- **Specific**: Provides enough detail for good results
- **Tested**: You've tested it and it works well
- **Documented**: Includes description and examples

## Code Contribution Guidelines

### Python Code

- Follow PEP 8 style guide
- Include docstrings for functions and classes
- Add type hints where appropriate
- Write unit tests for new functionality
- Keep functions focused and single-purpose

### Example

```python
def validate_prompt(prompt_data: dict) -> tuple[bool, str | None]:
    """
    Validate a prompt against the schema.
    
    Args:
        prompt_data: Dictionary containing prompt data
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Implementation
    pass
```

## Documentation Guidelines

### Markdown Files

- Use clear headings and structure
- Include code examples where relevant
- Keep language simple and accessible
- Add links to related resources

### README Updates

If your contribution requires README changes:
- Update the relevant section
- Maintain consistent formatting
- Keep it concise

## Review Process

### What Happens After You Submit

1. **Automated Checks**: Schema validation and linting
2. **Initial Review**: Maintainer reviews your contribution
3. **Feedback**: You may receive suggestions for improvements
4. **Approval**: Once approved, your contribution will be merged

### Response Time

- We aim to respond to all contributions within 5 business days
- Complex contributions may take longer to review

## Pull Request Template

```markdown
## Description
[Brief description of your contribution]

## Type of Change
- [ ] New prompt
- [ ] Prompt improvement
- [ ] Bug fix
- [ ] Documentation update
- [ ] New feature
- [ ] Other (please describe)

## Category
[If adding a prompt: education/creative/productivity/coding]

## Testing
- [ ] I have tested this prompt/code
- [ ] I have validated against the schema
- [ ] I have added examples

## Checklist
- [ ] My code/prompt follows the project guidelines
- [ ] I have updated documentation as needed
- [ ] I have added appropriate tags/metadata
- [ ] My contribution is well-documented

## Additional Notes
[Any additional information]
```

## Questions or Issues?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the contribution, not the person
- Help create a welcoming environment

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to AI Prompt Lab! 🚀
