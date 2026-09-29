"""Smoke test: the package imports and reports a version."""
import causal_price


def test_package_imports():
    assert causal_price.__version__
