import math
import re

import pytest
from hypothesis import given, assume
import hypothesis.strategies as st

from main import celsius_to_fahrenheit, fahrenheit_to_celsius, format_result, dispatch, CONVERTERS, parse_args


# --- Unit tests ---

def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0
    assert celsius_to_fahrenheit(-40) == -40.0


def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(32) == 0.0
    assert fahrenheit_to_celsius(212) == 100.0
    assert fahrenheit_to_celsius(-40) == -40.0


def test_format_result_trailing_zeros():
    assert format_result(100.0) == "100.00"
    assert format_result(37.8) == "37.80"


# --- Property-based tests ---

# Feature: unit-converter-cli, Property 2: celsius-to-fahrenheit formula
@given(st.floats(allow_nan=False, allow_infinity=False))
def test_celsius_to_fahrenheit_formula(v):
    """Property 2: Celsius-to-Fahrenheit formula correctness
    Validates: Requirements 1.1
    """
    assert celsius_to_fahrenheit(v) == (v * 9 / 5) + 32


# Feature: unit-converter-cli, Property 1: celsius-fahrenheit round-trip
@given(st.floats(allow_nan=False, allow_infinity=False, min_value=-1e15, max_value=1e15))
def test_celsius_fahrenheit_round_trip(v):
    """Property 1: Celsius–Fahrenheit round-trip
    Validates: Requirements 1.1, 2.1
    """
    assert math.isclose(fahrenheit_to_celsius(celsius_to_fahrenheit(v)), v, rel_tol=1e-9, abs_tol=1e-9)


# Feature: unit-converter-cli, Property 3: output 2 decimal places
@given(st.floats(allow_nan=False, allow_infinity=False))
def test_format_result_two_decimal_places(v):
    """Property 3: Output always has exactly 2 decimal places
    Validates: Requirements 1.2, 2.2, 3.1, 3.2
    """
    result = format_result(v)
    assert re.match(r"-?\d+\.\d{2}$", result), f"format_result({v!r}) = {result!r} does not match pattern"


# --- Task 5.2: Unit tests for parse_args ---

def test_parse_args_insufficient():
    with pytest.raises(ValueError):
        parse_args([])
    with pytest.raises(ValueError):
        parse_args(["temperature"])
    with pytest.raises(ValueError):
        parse_args(["temperature", "c2f"])


# --- Task 3.2: Unit tests for dispatch error cases ---

def test_dispatch_unknown_type():
    with pytest.raises(ValueError):
        dispatch("length", "m2ft", "1")


def test_dispatch_unknown_direction():
    with pytest.raises(ValueError):
        dispatch("temperature", "x2y", "1")


def test_dispatch_invalid_value():
    with pytest.raises(ValueError):
        dispatch("temperature", "c2f", "abc")


# Feature: unit-converter-cli, Property 4: non-numeric input rejected
@given(st.text())
def test_dispatch_non_numeric_rejected(s):
    """Property 4: Non-numeric input is always rejected
    Validates: Requirements 1.3, 2.3
    """
    try:
        float(s)
        assume(False)  # skip strings that are valid floats
    except ValueError:
        pass
    with pytest.raises(ValueError):
        dispatch("temperature", "c2f", s)


# Feature: unit-converter-cli, Property 5: unknown dispatch key rejected
@given(st.text(), st.text())
def test_dispatch_unknown_key_rejected(t, d):
    """Property 5: Unknown conversion type or direction is always rejected
    Validates: Requirements 4.1, 4.2
    """
    assume((t, d) not in CONVERTERS)
    with pytest.raises(ValueError):
        dispatch(t, d, "1")
