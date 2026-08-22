# Contributing to YouTube AI Automation

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive criticism
- Respect all contributors

## How to Contribute

### Reporting Bugs

1. **Check existing issues** - Avoid duplicates
2. **Create detailed bug report** with:
   - Clear title
   - Step-by-step reproduction
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Error logs and screenshots

### Suggesting Features

1. **Use issue templates** for feature requests
2. **Explain the use case** clearly
3. **Describe expected behavior**
4. **Note any alternatives** you've considered

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/youtube-ai-automation.git
   cd youtube-ai-automation
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow code style guidelines (see below)
   - Add tests for new functionality
   - Update documentation

4. **Commit with clear messages**
   ```bash
   git commit -m 'Add amazing feature'
   git commit -m 'Fix issue with video generation'
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Create Pull Request**
   - Clear title and description
   - Reference related issues
   - Include screenshots/examples if relevant

## Code Style Guidelines

### Python

```python
# Format with Black
black backend/

# Check with Flake8
flake8 backend/

# Follow PEP 8
# - 4 spaces for indentation
# - Max 79 characters per line
# - Docstrings for all functions
```

### JavaScript/React

```javascript
// Format with Prettier
npm run format

// Lint with ESLint
npm run lint

// Follow Airbnb style guide
// - 2 spaces for indentation
// - Use const/let, not var
// - Arrow functions when appropriate
```

### Commit Messages

```
# Format
<type>(<scope>): <subject>

<body>

<footer>

# Examples
feat(video): Add subtitle automation
fix(auth): Resolve YouTube OAuth issue
docs(readme): Update installation guide
refactor(llm): Improve prompt engineering
test(generator): Add video generation tests
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code refactoring
- `test` - Tests
- `chore` - Maintenance

## Development Setup

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/youtube-ai-automation.git
cd youtube-ai-automation
bash scripts/setup.sh

# Install dev dependencies
pip install black flake8 pylint

# Run tests
pytest

# Format code
black backend/
```

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_core.py::TestFlaskApp::test_health_endpoint

# Run with coverage
pytest --cov=backend tests/
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Include code examples where helpful
- Document new environment variables

## Areas for Contribution

### High Priority
- [ ] WebSocket support for real-time progress
- [ ] Batch video generation
- [ ] Advanced error handling
- [ ] Performance optimization

### Medium Priority
- [ ] Multi-language subtitle support
- [ ] Advanced image generation
- [ ] Analytics dashboard
- [ ] API documentation (Swagger)

### Nice to Have
- [ ] Mobile app (React Native)
- [ ] Cloud deployment guides
- [ ] Advanced scheduling features
- [ ] Webhook support

## Getting Help

- **Discussions** - Ask questions in GitHub Discussions
- **Issues** - Report bugs or request features
- **Wiki** - Check for additional documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making YouTube AI Automation better! 🎉
