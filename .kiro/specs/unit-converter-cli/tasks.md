# Implementation Plan: unit-converter-cli

## Overview

Implement a zero-runtime-dependency Python 3.12 CLI tool for unit conversion, starting with temperature (Celsius ↔ Fahrenheit). The implementation lives in `main.py` and follows the three-layer pipeline defined in the design: argument parsing → dispatch → converter → formatter. All commands use `uv run`.

## Tasks

- [ ] 1. Set up project structure and dev dependencies
  - Add `hypothesis` as a dev-only dependency in `pyproject.toml` under `[dependency-groups]` (e.g. `dev = ["hypothesis>=6"]`)
  - Create `tests/` directory with an empty `__init__.py`
  - Create `tests/test_converter.py` as the single test file
  - Verify `uv run pytest --version` works after adding `pytest` to dev deps
  - _Requirements: 5.1, 5.2_

- [ ] 2. Implement core conversion functions and formatter
  - [ ] 2.1 Implement `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, and `format_result` in `main.py`
    - `celsius_to_fahrenheit(value: float) -> float`: `(value * 9 / 5) + 32`
    - `fahrenheit_to_celsius(value: float) -> float`: `(value - 32) * 5 / 9`
    - `format_result(value: float) -> str`: `f"{value:.2f}"`
    - _Requirements: 1.1, 2.1, 3.1, 3.2_

  - [ ] 2.2 Write unit tests for conversion functions and formatter
    - `test_celsius_to_fahrenheit`: 0→32, 100→212, -40→-40
    - `test_fahrenheit_to_celsius`: 32→0, 212→100, -40→-40
    - `test_format_result_trailing_zeros`: `format_result(100.0)` → `"100.00"`, `format_result(37.8)` → `"37.80"`
    - _Requirements: 1.1, 2.1, 3.1, 3.2_

  - [ ]* 2.3 Write property test for celsius-to-fahrenheit formula correctness
    - **Property 2: Celsius-to-Fahrenheit formula correctness**
    - **Validates: Requirements 1.1**
    - Use `@given(st.floats(allow_nan=False, allow_infinity=False))`
    - Assert `celsius_to_fahrenheit(v) == (v * 9 / 5) + 32` for all valid floats

  - [ ]* 2.4 Write property test for round-trip consistency
    - **Property 1: Celsius–Fahrenheit round-trip**
    - **Validates: Requirements 1.1, 2.1**
    - Use `@given(st.floats(allow_nan=False, allow_infinity=False))`
    - Assert `fahrenheit_to_celsius(celsius_to_fahrenheit(v))` is within floating-point tolerance of `v`

  - [ ]* 2.5 Write property test for output decimal places
    - **Property 3: Output always has exactly 2 decimal places**
    - **Validates: Requirements 1.2, 2.2, 3.1, 3.2**
    - Use `@given(st.floats(allow_nan=False, allow_infinity=False))`
    - Assert `format_result(v)` matches the regex `-?\d+\.\d{2}`

- [ ] 3. Implement converter registry and dispatch
  - [ ] 3.1 Define `CONVERTERS` registry dict and implement `dispatch` in `main.py`
    - `CONVERTERS: dict[tuple[str, str], Callable[[float], float]]` mapping `("temperature", "c2f")` and `("temperature", "f2c")`
    - `dispatch(conversion_type, direction, raw_value)` looks up registry, parses float, raises `ValueError` for unknown keys or non-numeric input
    - _Requirements: 1.1, 2.1, 4.1, 4.2_

  - [ ]* 3.2 Write unit tests for dispatch error cases
    - `test_dispatch_unknown_type`: `dispatch("length", "m2ft", "1")` raises `ValueError`
    - `test_dispatch_unknown_direction`: `dispatch("temperature", "x2y", "1")` raises `ValueError`
    - `test_dispatch_invalid_value`: `dispatch("temperature", "c2f", "abc")` raises `ValueError`
    - _Requirements: 1.3, 2.3, 4.1, 4.2_

  - [ ]* 3.3 Write property test for non-numeric input rejection
    - **Property 4: Non-numeric input is always rejected**
    - **Validates: Requirements 1.3, 2.3**
    - Use `@given(st.text())` filtered to strings that cannot be parsed as float
    - Assert `dispatch("temperature", "c2f", s)` raises `ValueError`

  - [ ]* 3.4 Write property test for unknown dispatch key rejection
    - **Property 5: Unknown conversion type or direction is always rejected**
    - **Validates: Requirements 4.1, 4.2**
    - Use `@given(st.text(), st.text())` filtered to pairs not in `CONVERTERS`
    - Assert `dispatch(t, d, "1")` raises `ValueError`

- [ ] 4. Checkpoint — ensure all tests pass
  - Run `uv run pytest tests/` and confirm all tests pass; ask the user if any questions arise.

- [ ] 5. Implement argument parser and main entry point
  - [ ] 5.1 Implement `parse_args` in `main.py`
    - `parse_args(args: list[str]) -> tuple[str, str, str]`
    - Raises `ValueError` with usage message when `len(args) != 3`
    - _Requirements: 4.3_

  - [ ]* 5.2 Write unit tests for `parse_args`
    - `test_parse_args_insufficient`: `parse_args([])`, `parse_args(["temperature"])`, `parse_args(["temperature", "c2f"])` all raise `ValueError`
    - _Requirements: 4.3_

  - [ ] 5.3 Implement `main` entry point in `main.py`
    - Reads `sys.argv[1:]`, calls `parse_args`, calls `dispatch`, prints `format_result(result)` to stdout
    - Catches `ValueError` / `KeyError`, writes message to `sys.stderr`, calls `sys.exit(1)`
    - Wire `if __name__ == "__main__": main()` guard
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 4.1, 4.2, 4.3, 5.2_

- [ ] 6. Final checkpoint — end-to-end smoke tests and validation
  - Run `uv run main.py temperature c2f 0` and assert output is `32.00` with exit code 0
  - Run `uv run main.py temperature f2c 212` and assert output is `100.00` with exit code 0
  - Run `uv run main.py temperature c2f abc` and assert exit code is non-zero
  - Verify `pyproject.toml` has no runtime dependencies (only dev deps for `hypothesis` and `pytest`)
  - Run `uv run pytest tests/` and confirm all tests pass; ask the user if any questions arise.
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2, 4.3, 5.1, 5.2_

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- All commands use `uv run` — no global Python or pip required
- `hypothesis` is a dev-only dependency and does not violate Requirement 5 (no runtime external deps)
- Each property test references the design property number it validates
- Checkpoints ensure incremental validation before wiring everything together
