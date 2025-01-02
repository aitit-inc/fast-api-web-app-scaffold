"""Example test case."""
from typing import Any


def setup_function(_function: Any) -> None:
    """Set up the test environment."""
    print("Setting up the test environment...")


def teardown_function(_function: Any) -> None:
    """Tear down the test environment."""
    print("Tearing down the test environment...")


def test_simple_assert() -> None:
    """Test a simple assert."""
    print("Running the test...")
    assert True
