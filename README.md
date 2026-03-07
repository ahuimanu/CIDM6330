# CIDM 6330 Spring 2026

This repository contains supplemental materials and code for CIDM 6330, Spring 2026.

## Primary Text

We are using *Fundamentals of Software Architecture, 2nd Edition* as our guide.

## Course Materials

The [docs](docs/README.MD) folder contains supplemental readings and foundational content organized across four Foundations covering software architecture concepts and distributed systems.

## Resources

- [Git Crash Course](https://gist.github.com/brandon1024/14b5f9fcfd982658d01811ee3045ff1e) - Good resource for beginners
- [MDN Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) - Overview and tutorial for Django

## Python Tooling

This course uses [Astral](https://astral.sh/) tools for Python development:

- **uv** - Package and environment management
- **ruff** - Linting and formatting
- **ty** - Type checking

To create a virtual environment and install dependencies:

```bash
uv venv
uv pip install -r requirements.txt
```
