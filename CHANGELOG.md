# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced validator with warnings and directory validation
- CLI tool with create, validate, list, and stats commands
- GitHub Actions workflow for automated validation
- 10 sample prompts across all categories
- Comprehensive test suite with pytest
- Setup guide documentation
- Enhanced README with badges and detailed instructions
- Development dependencies (pytest, black, flake8, mypy)

### Changed
- Improved prompt schema with better validation rules
- Updated validator to return warnings along with validation results
- Enhanced error messages for better debugging

### Fixed
- ID pattern validation to enforce lowercase and hyphens
- Score validation to enforce 1-5 range

## [0.1.0] - 2025-10-10

### Added
- Initial project structure
- Core prompt schema (prompt_schema.json)
- Basic prompt validator
- Documentation (PROMPT_GUIDE, EVALUATION_GUIDE, CONTRIBUTING)
- Four prompt categories (education, creative, productivity, coding)
- First sample prompt (edu-001)
- MIT License
- .gitignore for Python projects
