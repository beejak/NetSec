# Contributing to NetSec-Core

Thank you for your interest in contributing to NetSec-Core! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of network security

### Development Setup

1. **Fork the repository**

2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/netsec-core.git
   cd netsec-core
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pip install -e .
   ```

5. **Run tests:**
   ```bash
   pytest
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation

### 3. Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **mypy** for type checking

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

### 4. Write Tests

- Add unit tests for new features
- Add integration tests for API/CLI
- Ensure all tests pass
- Aim for >80% code coverage

```bash
# Run tests
pytest

# With coverage
pytest --cov=netsec_core --cov-report=html
```

### 5. Update Documentation

- Update README if needed
- Add docstrings to new functions
- Update CHANGELOG.md
- Add examples if applicable

### 6. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: fix bug description"
```

**Commit Message Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted (black)
- [ ] No linting errors (ruff)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow format

### PR Description

Include:
- Description of changes
- Related issues (if any)
- Testing performed
- Screenshots (if UI changes)

## Project Structure

```
netsec-core/
├── src/netsec_core/
│   ├── api/          # FastAPI routes
│   ├── cli/          # CLI commands
│   ├── core/         # Core scanners
│   ├── llm/          # LLM integration
│   ├── remediation/  # Remediation system
│   └── utils/        # Utilities
├── tests/            # Test suite
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
└── docs/             # Documentation
```

## Adding New Features

### 1. New Scanner

1. Create scanner in `src/netsec_core/core/`
2. Add API routes in `src/netsec_core/api/routes/`
3. Add CLI commands in `src/netsec_core/cli/commands/`
4. Add tests in `tests/`
5. Update documentation

### 2. New API Endpoint

1. Add route in appropriate route module
2. Add Pydantic models if needed
3. Add tests
4. Update API documentation

### 3. New CLI Command

1. Add command in appropriate command module
2. Add help text
3. Add tests
4. Update CLI documentation

## Testing Guidelines

### Unit Tests

- Test individual functions/methods
- Mock external dependencies
- Test edge cases
- Test error handling

### Integration Tests

- Test API endpoints
- Test CLI commands
- Test module interactions
- Test error scenarios

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_dns_scanner.py

# With coverage
pytest --cov=netsec_core --cov-report=term-missing

# Verbose output
pytest -v
```

## Documentation

### Code Documentation

- Use docstrings for all functions/classes
- Follow Google or NumPy style
- Include parameter descriptions
- Include return value descriptions
- Include example usage

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Update QUICKSTART.md if needed
- Update DEPLOYMENT.md for deployment changes

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Error messages/logs

### Feature Requests

Include:
- Description of the feature
- Use case/justification
- Proposed implementation (if any)
- Alternatives considered

## Questions?

- Open an issue for questions
- Check existing issues first
- Be patient for responses

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for contributing to NetSec-Core! 🎉
