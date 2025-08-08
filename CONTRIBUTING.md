# Contributing to Markdown Diagram Fixer

Thank you for your interest in contributing! We welcome contributions from the community and are grateful for any help you can provide.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. **Search existing issues** to avoid duplicates
2. **Create a new issue** using one of our issue templates
3. **Provide clear details** including:
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Sample diagrams that demonstrate the issue
   - Your environment (OS, Python version)

### Contributing Code

We welcome pull requests! Here's how to get started:

#### Quick Start

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone git@github.com:YOUR-USERNAME/markdown-diagram-fixer.git
   cd markdown-diagram-fixer
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

#### Making Changes

1. **Follow the existing code style** and patterns
2. **Test your changes** thoroughly:
   ```bash
   # Test the main tool
   python3 precision_diagram_fixer.py example_diagram.txt
   
   # Test pandoc integration
   cat dev-archive/test-data/test_quiet.md | python3 pandoc_preprocessor.py
   
   # Test with complex diagrams
   python3 precision_diagram_fixer.py dev-archive/test-data/extracted_doc_diagram_2.txt
   ```
3. **Add tests** for new functionality using the existing test data patterns
4. **Update documentation** if needed (README.md, docstrings)

#### Submitting Changes

1. **Commit your changes** with clear, descriptive messages:
   ```bash
   git add .
   git commit -m "Fix alignment issue with nested boxes
   
   - Improve box detection tolerance for misaligned corners
   - Add test case for overlapping box structures
   - Resolves #123"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/examples if applicable
   - Test results

## Development Guidelines

### Code Style

- Follow existing Python conventions and patterns
- Use clear, descriptive variable and function names  
- Add docstrings for new functions and classes
- Keep functions focused and reasonably sized
- Comment complex algorithms or business logic

### Testing

- Test with various diagram types and complexities
- Include both positive and negative test cases
- Test error conditions and edge cases
- Verify pandoc integration works correctly
- Test with both simple and complex real-world diagrams

### Performance

- The tool should handle diagrams efficiently (typically < 1 second for complex diagrams)
- Avoid algorithms with exponential complexity
- Test with large diagrams when making algorithmic changes

### Documentation

- Update README.md for new features or usage changes
- Add examples for new functionality
- Update CLAUDE.md for development-specific changes
- Include clear commit messages and PR descriptions

## Project Structure

```
markdown-diagram-fixer/
├── precision_diagram_fixer.py    # Main tool
├── pandoc_preprocessor.py         # Pandoc integration
├── example_diagram.txt            # Sample for testing
├── README.md                      # User documentation
├── CONTRIBUTING.md               # This file
├── SECURITY.md                   # Security policy
├── LICENSE                       # MIT license
└── dev-archive/                  # Development artifacts
    ├── test-data/               # Test diagrams
    ├── debug-tools/             # Analysis utilities
    ├── experiments/             # Prototype implementations
    └── documentation/           # Development notes
```

## Types of Contributions Needed

### High Priority
- **Bug fixes** for diagram parsing or alignment issues
- **Performance improvements** for large or complex diagrams
- **Test cases** for edge cases or specific diagram types
- **Documentation improvements** with clearer examples

### Medium Priority
- **New diagram formats** support (ASCII art variations)
- **Enhanced pandoc integration** features
- **Error handling** improvements
- **Code refactoring** for maintainability

### Nice to Have
- **Additional output formats** or options
- **Integration** with other documentation tools
- **Performance benchmarking** tools
- **Automated testing** infrastructure

## Getting Help

- **Documentation**: Start with README.md and code comments
- **Development Notes**: Check dev-archive/documentation/ for algorithm details  
- **Issues**: Search existing issues for similar problems
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Contact**: Reach out to [@andrewyager](https://github.com/andrewyager) for guidance

## Code of Conduct

- Be respectful and constructive in all interactions
- Focus on the technical merits of contributions
- Help newcomers get started with clear feedback
- Maintain a welcoming environment for all contributors

## Recognition

Contributors will be:
- Credited in release notes for significant contributions
- Listed in GitHub's contributor graphs
- Mentioned in README.md for major features (optional)

Thank you for contributing to make diagram fixing better for everyone! 🎉