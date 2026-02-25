# Contributing to Business Analytics Dashboard

Thank you for your interest in contributing to the Business Analytics Dashboard! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please report it by creating an issue on GitHub with the following information:

- **Bug Description**: Clear and concise description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: Python version, OS, and library versions
- **Screenshots**: If applicable, include screenshots
- **Additional Context**: Any other relevant information

### Suggesting Features

We welcome feature suggestions! Please create an issue with:

- **Feature Description**: Clear description of the proposed feature
- **Use Case**: Why this feature would be useful
- **Implementation Ideas**: How you think it could be implemented
- **Priority**: Low, Medium, or High priority

### Submitting Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/business-analytics-dashboard.git
   cd business-analytics-dashboard
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   python -m pytest tests/
   black --check *.py
   flake8 *.py
   ```

5. **Commit Your Changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Include screenshots if applicable

## 📝 Coding Standards

### Python Code Style

We follow PEP 8 and use the following tools:

- **Black**: Code formatting
- **flake8**: Linting
- **pytest**: Testing

#### Code Formatting

```bash
# Format code
black *.py

# Check formatting
black --check *.py

# Lint code
flake8 *.py
```

#### Naming Conventions

- **Functions and Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private Methods**: `_leading_underscore`

#### Documentation

```python
def calculate_rsi(data, window=14):
    """
    Calculate Relative Strength Index (RSI) for technical analysis.
    
    Args:
        data (pd.Series): Price data series
        window (int): RSI calculation window (default: 14)
    
    Returns:
        pd.Series: RSI values
    
    Raises:
        ValueError: If data is insufficient or window is invalid
    
    Example:
        >>> rsi = calculate_rsi(df['Close'], window=14)
        >>> print(rsi.tail())
    """
    pass
```

### File Organization

```
project/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── examples/               # Example scripts
├── config/                 # Configuration files
└── scripts/                # Utility scripts
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_analytics.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Writing Tests

```python
import pytest
import pandas as pd
from src.analytics import calculate_returns

def test_calculate_returns():
    """Test returns calculation function."""
    # Setup
    prices = pd.Series([100, 105, 102, 108, 110])
    expected = pd.Series([0.05, -0.0286, 0.0588, 0.0185])
    
    # Execute
    result = calculate_returns(prices)
    
    # Assert
    pd.testing.assert_series_equal(result.round(4), expected)
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Include integration tests
- Document test scenarios

## 📚 Documentation

### Updating Documentation

- **README.md**: Update for new features or changes
- **API Documentation**: Update docstrings for new functions
- **CHANGELOG.md**: Add entries for all changes
- **Examples**: Add example scripts for new features

### Documentation Style

- Use clear, concise language
- Include code examples
- Provide step-by-step instructions
- Use proper markdown formatting

## 🔄 Development Workflow

### Branch Strategy

- **main**: Stable, production-ready code
- **develop**: Integration branch for features
- **feature/***: Feature branches
- **bugfix/***: Bug fix branches
- **hotfix/***: Critical fixes for production

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(analytics): add MACD indicator calculation
fix(excel): resolve cell formatting issue
docs(readme): update installation instructions
```

### Code Review Process

1. **Self-Review**: Review your own code before submitting
2. **Peer Review**: Another developer reviews the changes
3. **Testing**: Ensure all tests pass
4. **Documentation**: Update relevant documentation
5. **Merge**: Merge after approval

## 🛠️ Development Environment

### Setup

```bash
# Clone repository
git clone https://github.com/your-username/business-analytics-dashboard.git
cd business-analytics-dashboard

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 📋 Issue Templates

### Bug Report Template

```markdown
**Bug Description**
A clear and concise description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Actual Behavior**
A clear description of what actually happened.

**Environment**
- OS: [e.g. Windows 10, macOS 11.0]
- Python Version: [e.g. 3.9.0]
- Library Versions: [e.g. pandas 1.3.0]

**Additional Context**
Add any other context about the problem here.
```

### Feature Request Template

```markdown
**Feature Description**
A clear and concise description of the feature.

**Use Case**
Describe why this feature would be useful.

**Proposed Solution**
If you have ideas on how to implement it, describe them here.

**Alternatives Considered**
Describe any alternative solutions you've considered.

**Additional Context**
Add any other context or screenshots about the feature request here.
```

## 🎯 Project Goals

### Short-term Goals
- [ ] Add unit tests for all analytics functions
- [ ] Improve error handling and logging
- [ ] Add more technical indicators
- [ ] Enhance Excel formatting options

### Long-term Goals
- [ ] Web dashboard interface
- [ ] Real-time data integration
- [ ] Machine learning predictions
- [ ] Multi-asset portfolio analysis

## 🏆 Recognition

### Contributors

We recognize and appreciate all contributors. Contributors will be:

- Listed in the README.md
- Mentioned in release notes
- Invited to contributor discussions
- Eligible for project maintainer roles

### Recognition Criteria

- **Bug Fixers**: Reported and fixed bugs
- **Feature Contributors**: Added new features
- **Documentation**: Improved documentation
- **Community**: Helped others in discussions
- **Testing**: Improved test coverage

## 📞 Getting Help

### Resources

- **Documentation**: Check the README and docs folder
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Join GitHub Discussions for questions
- **Email**: Contact the development team

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: Private or sensitive matters

## 📄 Legal

### License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and professional
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Be inclusive of all skill levels and backgrounds

## 🚀 Release Process

### Version Management

We follow Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG is updated
- [ ] Version is bumped
- [ ] Release notes are written
- [ ] Tag is created
- [ ] Release is published

---

Thank you for contributing to the Business Analytics Dashboard! Your contributions help make this project better for everyone. 🎉
