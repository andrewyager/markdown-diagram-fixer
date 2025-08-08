# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of our users seriously. If you believe you have found a security vulnerability in this project, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them privately using one of these methods:

1. **GitHub Security Advisories** (recommended): Use GitHub's private vulnerability reporting feature by going to the Security tab of this repository and clicking "Report a vulnerability"

2. **Email**: Contact the project maintainer directly through GitHub

### What to Include

Please include the following information in your report:

- A description of the vulnerability and its potential impact
- Steps to reproduce the issue
- Any relevant code snippets or proof-of-concept
- Your assessment of the severity
- Any suggested fixes or mitigations

### Response Process

1. **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
2. **Assessment**: We will assess the vulnerability and determine its severity within 5 business days
3. **Fix Development**: We will work on a fix and coordinate disclosure timeline with you
4. **Release**: We will release a patched version and publish a security advisory
5. **Credit**: We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Considerations

This tool processes text input and generates text output. Key security considerations:

### Input Validation
- The tool only processes UTF-8 text containing ASCII diagram characters
- No code execution or file system operations beyond reading input files
- No network operations or external dependencies

### File Operations
- Only reads specified input files
- Only writes output files in the same directory as input (with `_fixed.txt` suffix)
- No arbitrary file system access

### Pandoc Integration
- The pandoc preprocessor reads from stdin and writes to stdout only
- No temporary file creation or persistent state
- Error conditions fail safely by outputting original content unchanged

## Best Practices for Contributors

- Always validate input parameters and handle edge cases gracefully
- Avoid adding external dependencies without security review
- Use secure coding practices and follow the existing code patterns
- Test error conditions and ensure graceful failure modes

## Security Updates

Security updates will be:
- Released as patch versions (x.x.1, x.x.2, etc.)
- Documented in the changelog with clear security impact description
- Announced through GitHub security advisories
- Tagged with appropriate severity levels

## Contact

For security-related questions or concerns, please contact:
- Project Maintainer: [@andrewyager](https://github.com/andrewyager)

---

Thank you for helping keep our project and community safe!