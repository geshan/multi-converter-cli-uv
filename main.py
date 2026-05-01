from typing import Callable


def celsius_to_fahrenheit(value: float) -> float:
    return (value * 9 / 5) + 32


def fahrenheit_to_celsius(value: float) -> float:
    return (value - 32) * 5 / 9


def format_result(value: float) -> str:
    return f"{value:.2f}"


CONVERTERS: dict[tuple[str, str], Callable[[float], float]] = {
    ("temperature", "c2f"): celsius_to_fahrenheit,
    ("temperature", "f2c"): fahrenheit_to_celsius,
}


def dispatch(conversion_type: str, direction: str, raw_value: str) -> float:
    # Check conversion type
    supported_types = {t for t, _ in CONVERTERS}
    if conversion_type not in supported_types:
        raise ValueError(
            f"Unknown conversion type '{conversion_type}'. Supported: {', '.join(sorted(supported_types))}"
        )
    # Check direction
    supported_directions = {d for t, d in CONVERTERS if t == conversion_type}
    if direction not in supported_directions:
        raise ValueError(
            f"Unknown direction '{direction}' for '{conversion_type}'. Supported: {', '.join(sorted(supported_directions))}"
        )
    # Parse value
    try:
        value = float(raw_value)
    except ValueError:
        raise ValueError(f"Invalid value '{raw_value}': must be a number")
    return CONVERTERS[(conversion_type, direction)](value)


def parse_args(args: list[str]) -> tuple[str, str, str]:
    if len(args) != 3:
        raise ValueError("Usage: uv run main.py <type> <direction> <value>")
    return args[0], args[1], args[2]


def main() -> None:
    import sys
    args = sys.argv[1:]
    try:
        conversion_type, direction, raw_value = parse_args(args)
        result = dispatch(conversion_type, direction, raw_value)
        print(format_result(result))
    except ValueError as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
