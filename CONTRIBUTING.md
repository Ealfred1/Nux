# Contributing to NuxAI

Thank you for your interest in contributing to NuxAI! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and encourage diverse perspectives
- Focus on constructive feedback
- Help others learn and grow

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/nuxai.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages: `git commit -m "Add: feature description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Overlay

```bash
cd overlay
flutter pub get
flutter run -d linux
```

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Dart (Overlay)

- Follow Dart style guide
- Use `flutter format` before committing
- Add comments for complex logic
- Keep widgets small and focused

## Commit Messages

Use conventional commit format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example: `feat: add weather command support`

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Include test coverage for bug fixes

## Pull Request Process

1. Update README.md if needed
2. Update documentation for new features
3. Ensure code follows style guidelines
4. All tests must pass
5. Get at least one code review
6. Squash commits if requested

## Feature Requests

Open an issue with:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach

## Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- System information (OS, Python version, etc.)
- Logs if applicable

## Questions?

- Open a Discussion on GitHub
- Join our community chat
- Check existing issues and documentation

Thank you for contributing to NuxAI! 🎤

