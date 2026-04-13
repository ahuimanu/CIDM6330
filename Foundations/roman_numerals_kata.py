"""
Roman Numerals Kata

Functions:
- int_to_roman(number): int -> Roman numeral
- roman_to_int(roman): Roman numeral -> int

Constraints:
- supports 1..3000
- rejects non-canonical numerals
"""

ROMAN_PAIRS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

MIN_VALUE = 1
MAX_VALUE = 3000


def int_to_roman(number: int) -> str:
    """Convert an integer to a Roman numeral."""
    _validate_int(number)

    remaining = number
    parts = []

    for value, numeral in ROMAN_PAIRS:
        count, remaining = divmod(remaining, value)
        if count:
            parts.append(numeral * count)

    return "".join(parts)


def roman_to_int(roman: str) -> int:
    """Convert a Roman numeral to an integer."""
    normalized = _normalize_roman(roman)

    total = 0
    previous = 0
    for char in reversed(normalized):
        value = ROMAN_VALUES[char]
        if value < previous:
            total -= value
        else:
            total += value
        previous = value

    if not (MIN_VALUE <= total <= MAX_VALUE):
        raise ValueError(f"Roman numeral out of range: {roman}")

    # Ensure canonical form (rejects invalid patterns like 'IC', 'IIII')
    if int_to_roman(total) != normalized:
        raise ValueError(f"Invalid Roman numeral format: {roman}")

    return total


def _validate_int(number: int) -> None:
    if not isinstance(number, int):
        raise ValueError(f"Number must be an integer, got {type(number).__name__}")
    if not (MIN_VALUE <= number <= MAX_VALUE):
        raise ValueError(
            f"Number must be between {MIN_VALUE} and {MAX_VALUE}, got {number}"
        )


def _normalize_roman(roman: str) -> str:
    if not isinstance(roman, str):
        raise ValueError(f"Roman numeral must be a string, got {type(roman).__name__}")

    normalized = roman.strip().upper()
    if not normalized:
        raise ValueError("Roman numeral cannot be empty")

    for char in normalized:
        if char not in ROMAN_VALUES:
            raise ValueError(f"Invalid Roman numeral character: {char}")

    return normalized


if __name__ == "__main__":
    test_cases = [
        (1, "I"),
        (2, "II"),
        (3, "III"),
        (4, "IV"),
        (5, "V"),
        (6, "VI"),
        (7, "VII"),
        (8, "VIII"),
        (9, "IX"),
        (10, "X"),
        (40, "XL"),
        (44, "XLIV"),
        (90, "XC"),
        (99, "XCIX"),
        (400, "CD"),
        (900, "CM"),
        (1994, "MCMXCIV"),
        (2024, "MMXXIV"),
        (3000, "MMM"),
    ]

    print("Testing int_to_roman...")
    for number, expected in test_cases:
        result = int_to_roman(number)
        status = "OK" if result == expected else "FAIL"
        print(f"{number} -> {result} {status}")

    print("\nTesting roman_to_int...")
    for expected, roman in test_cases:
        result = roman_to_int(roman)
        status = "OK" if result == expected else "FAIL"
        print(f"{roman} -> {result} {status}")

    print("\nTesting round-trip...")
    for number, _ in test_cases:
        back = roman_to_int(int_to_roman(number))
        status = "OK" if back == number else "FAIL"
        print(f"{number} -> {int_to_roman(number)} -> {back} {status}")
