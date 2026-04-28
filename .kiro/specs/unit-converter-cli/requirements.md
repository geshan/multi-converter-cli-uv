# Requirements Document

## Introduction

A CLI tool written in Python (3.12+) with no external dependencies, managed via `uv`. The first conversion module is a temperature converter supporting bidirectional conversion between Celsius and Fahrenheit. Results are rounded to 2 decimal places. The tool is invoked via `uv run main.py` and accepts conversion type, value, and direction as command-line arguments.

## Glossary

- **CLI**: Command-Line Interface — the tool is operated entirely from a terminal.
- **Converter**: The component responsible for performing a unit conversion calculation.
- **Temperature_Converter**: The sub-component of the Converter that handles Celsius ↔ Fahrenheit conversions.
- **Input_Value**: The numeric value supplied by the user to be converted.
- **Output_Value**: The numeric result produced after conversion, rounded to 2 decimal places.
- **Conversion_Type**: The category of conversion requested (e.g., `temperature`).
- **Direction**: The conversion direction specified by the user (e.g., `c2f` for Celsius to Fahrenheit, `f2c` for Fahrenheit to Celsius).

## Requirements

### Requirement 1: Temperature Conversion — Celsius to Fahrenheit

**User Story:** As a developer, I want to convert a Celsius value to Fahrenheit from the command line, so that I can quickly obtain the equivalent temperature without writing custom code.

#### Acceptance Criteria

1. WHEN the user runs `uv run main.py temperature c2f <value>`, THE Temperature_Converter SHALL compute the Fahrenheit equivalent using the formula `(value × 9/5) + 32`.
2. WHEN the conversion is complete, THE Temperature_Converter SHALL print the Output_Value rounded to 2 decimal places to standard output.
3. IF the supplied Input_Value is not a valid number, THEN THE CLI SHALL print a descriptive error message to standard error and exit with a non-zero exit code.

---

### Requirement 2: Temperature Conversion — Fahrenheit to Celsius

**User Story:** As a developer, I want to convert a Fahrenheit value to Celsius from the command line, so that I can quickly obtain the equivalent temperature without writing custom code.

#### Acceptance Criteria

1. WHEN the user runs `uv run main.py temperature f2c <value>`, THE Temperature_Converter SHALL compute the Celsius equivalent using the formula `(value − 32) × 5/9`.
2. WHEN the conversion is complete, THE Temperature_Converter SHALL print the Output_Value rounded to 2 decimal places to standard output.
3. IF the supplied Input_Value is not a valid number, THEN THE CLI SHALL print a descriptive error message to standard error and exit with a non-zero exit code.

---

### Requirement 3: Output Precision

**User Story:** As a developer, I want all conversion results to be displayed with exactly 2 decimal places, so that the output is consistent and predictable.

#### Acceptance Criteria

1. THE Temperature_Converter SHALL round all Output_Values to 2 decimal places before printing.
2. THE Temperature_Converter SHALL display trailing zeros where necessary to always show exactly 2 decimal places (e.g., `100.00`, `37.80`).

---

### Requirement 4: CLI Argument Validation

**User Story:** As a developer, I want the CLI to validate my input and provide clear error messages, so that I can correct mistakes quickly.

#### Acceptance Criteria

1. IF the user provides an unrecognised Conversion_Type, THEN THE CLI SHALL print a descriptive error message listing the supported conversion types and exit with a non-zero exit code.
2. IF the user provides an unrecognised Direction for a given Conversion_Type, THEN THE CLI SHALL print a descriptive error message listing the supported directions for that type and exit with a non-zero exit code.
3. IF the user provides insufficient arguments, THEN THE CLI SHALL print a usage message to standard error and exit with a non-zero exit code.

---

### Requirement 5: No External Dependencies

**User Story:** As a developer, I want the tool to rely only on the Python standard library, so that it can be run in any environment without additional package installation.

#### Acceptance Criteria

1. THE CLI SHALL use only Python standard library modules (no third-party packages).
2. THE CLI SHALL be executable via `uv run main.py <args>` on Python 3.12 or later.
