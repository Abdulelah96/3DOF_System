import nox

# Use Python 3.11 (or 3.12 if installed)
@nox.session(python="3.11")
def tests(session):
    """Run all tests and coverage."""
    # Install the package in editable mode with dev dependencies (if defined)
    session.run("pip", "install", "-e", ".")
    # Install testing packages
    session.run("pip", "install", "pytest", "pytest-cov")
    # Run tests
    session.run("pytest", "./tests", "--cov=three_dof_system", "--cov-report=term-missing")


@nox.session(python="3.11")
def lint(session):
    """Check code style with flake8."""
    session.run("pip", "install", "flake8")
    session.run("flake8", "./three_dof_system", "./tests", "--max-line-length=127")


@nox.session(python="3.11")
def format(session):
    """Format code with isort and black."""
    session.run("pip", "install", "isort", "black")
    session.run("isort", "./three_dof_system", "./tests")
    session.run("black", "./three_dof_system", "./tests")
