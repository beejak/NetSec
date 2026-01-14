# Contributing to NetSec-Cloud

Thank you for your interest in contributing to NetSec-Cloud!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a branch for your changes
4. Make your changes
5. Add tests
6. Submit a pull request

## Development Setup

```bash
pip install -r requirements.txt
pip install -e ".[dev]"
pytest
```

## Code Style

- Use black for formatting
- Use ruff for linting
- Add type hints
- Write docstrings

## Adding New Checks

1. Create check class in `checks/`
2. Implement check logic
3. Add tests
4. Update documentation

## Adding Provider Support

1. Create provider class in `providers/`
2. Implement required methods
3. Add authentication
4. Add security checks
5. Add tests

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_providers.py

# With coverage
pytest --cov=netsec_cloud
```

## Documentation

- Update README for user-facing changes
- Update architecture docs for design changes
- Add examples for new features

## Questions?

Open an issue for questions or discussions.
