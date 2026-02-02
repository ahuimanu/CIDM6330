"""
Roman Numerals Kata - Clean Implementation with TDD Principles

This implementation focuses on:
- Readability and clarity
- Comprehensive test coverage
- Logical separation of concerns
- Clean data structures
"""

from typing import ClassVar


class RomanNumeralConverter:
    """Converts between integers and Roman numerals."""

    # Ordered from largest to smallest - critical for the algorithm
    ROMAN_MAP: ClassVar[list[tuple[int, str]]] = [
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

    # Reverse mapping for parsing
    ROMAN_VALUES: ClassVar[dict[str, int]] = {
        numeral: value for value, numeral in ROMAN_MAP if len(numeral) == 1
    }

    MIN_VALUE = 1
    MAX_VALUE = 3000

    @classmethod
    def to_roman(cls, number: int) -> str:
        """
        Convert an integer to a Roman numeral.

        Args:
            number: Integer between 1 and 3000

        Returns:
            Roman numeral string

        Raises:
            ValueError: If number is outside valid range
        """
        cls._validate_input(number)

        result = []
        remaining = number

        for value, numeral in cls.ROMAN_MAP:
            while remaining >= value:
                result.append(numeral)
                remaining -= value

        return "".join(result)

    @classmethod
    def from_roman(cls, roman: str) -> int:
        """
        Convert a Roman numeral to an integer.

        Args:
            roman: Roman numeral string

        Returns:
            Integer value

        Raises:
            ValueError: If roman contains invalid characters
        """
        cls._validate_roman(roman)

        total = 0
        previous_value = 0

        # Process from right to left
        for char in reversed(roman):
            current_value = cls.ROMAN_VALUES[char]

            # If current value is less than previous, subtract it (e.g., IV, IX)
            if current_value < previous_value:
                total -= current_value
            else:
                total += current_value

            previous_value = current_value

        return total

    @classmethod
    def _validate_input(cls, number: int) -> None:
        """Validate that the input number is within acceptable range."""
        if not isinstance(number, int):
            raise ValueError(f"Number must be an integer, got {type(number).__name__}")

        if not (cls.MIN_VALUE <= number <= cls.MAX_VALUE):
            raise ValueError(
                f"Number must be between {cls.MIN_VALUE} and {cls.MAX_VALUE}, got "
                f"{number}"
            )

    @classmethod
    def _validate_roman(cls, roman: str) -> None:
        """Validate that the Roman numeral string contains only valid characters."""
        if not isinstance(roman, str):
            raise ValueError(
                f"Roman numeral must be a string, got {type(roman).__name__}"
            )

        if not roman:
            raise ValueError("Roman numeral cannot be empty")

        valid_chars = set(cls.ROMAN_VALUES.keys())
        for char in roman:
            if char not in valid_chars:
                raise ValueError(f"Invalid Roman numeral character: '{char}'")


# ============================================
# TESTS
# ============================================


def test_basic_conversions():
    """Test basic single-letter Roman numerals."""
    test_cases = [
        (1, "I"),
        (5, "V"),
        (10, "X"),
        (50, "L"),
        (100, "C"),
        (500, "D"),
        (1000, "M"),
    ]
    for number, expected in test_cases:
        result = RomanNumeralConverter.to_roman(number)
        assert result == expected, f"Expected {expected}, got {result}"
        # Test round-trip
        back = RomanNumeralConverter.from_roman(result)
        assert back == number, f"Round-trip failed: {number} -> {result} -> {back}"
    print("[PASS] Basic conversions passed")


def test_additive_combinations():
    """Test additive combinations (III, VIII, etc.)."""
    test_cases = [
        (2, "II"),
        (3, "III"),
        (6, "VI"),
        (7, "VII"),
        (8, "VIII"),
        (20, "XX"),
        (30, "XXX"),
        (60, "LX"),
        (70, "LXX"),
        (80, "LXXX"),
        (200, "CC"),
        (300, "CCC"),
        (600, "DC"),
        (700, "DCC"),
        (800, "DCCC"),
        (2000, "MM"),
        (3000, "MMM"),
    ]
    for number, expected in test_cases:
        result = RomanNumeralConverter.to_roman(number)
        assert result == expected, f"Expected {expected}, got {result}"
        back = RomanNumeralConverter.from_roman(result)
        assert back == number
    print("[PASS] Additive combinations passed")


def test_subtractive_notation():
    """Test subtractive notation (IV, IX, XL, etc.)."""
    test_cases = [
        (4, "IV"),
        (9, "IX"),
        (40, "XL"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (44, "XLIV"),
        (99, "XCIX"),
        (444, "CDXLIV"),
        (999, "CMXCIX"),
    ]
    for number, expected in test_cases:
        result = RomanNumeralConverter.to_roman(number)
        assert result == expected, f"Expected {expected}, got {result}"
        back = RomanNumeralConverter.from_roman(result)
        assert back == number
    print("[PASS] Subtractive notation passed")


def test_complex_numbers():
    """Test complex numbers combining all patterns."""
    test_cases = [
        (1994, "MCMXCIV"),
        (2023, "MMXXIII"),
        (1776, "MDCCLXXVI"),
        (1989, "MCMLXXXIX"),
        (2024, "MMXXIV"),
        (1492, "MCDXCII"),
        (1066, "MLXVI"),
        (1666, "MDCLXVI"),
    ]
    for number, expected in test_cases:
        result = RomanNumeralConverter.to_roman(number)
        assert result == expected, f"Expected {expected}, got {result}"
        back = RomanNumeralConverter.from_roman(result)
        assert back == number
    print("[PASS] Complex numbers passed")


def test_edge_cases():
    """Test boundary conditions and error handling."""
    # Boundaries
    assert RomanNumeralConverter.to_roman(1) == "I"
    assert RomanNumeralConverter.to_roman(3000) == "MMM"

    # Errors
    try:
        RomanNumeralConverter.to_roman(0)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    try:
        RomanNumeralConverter.to_roman(3001)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    try:
        RomanNumeralConverter.to_roman(-1)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    try:
        RomanNumeralConverter.to_roman(3.5)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    try:
        RomanNumeralConverter.from_roman("ABC")
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    try:
        RomanNumeralConverter.from_roman("")
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    print("[PASS] Edge cases passed")


def run_all_tests():
    """Run all test suites."""
    print("Running Roman Numeral Tests...\n")
    test_basic_conversions()
    test_additive_combinations()
    test_subtractive_notation()
    test_complex_numbers()
    test_edge_cases()
    print("\n[PASS] All tests passed!")


if __name__ == "__main__":
    # Demonstration
    print("=" * 50)
    print("ROMAN NUMERAL CONVERTER")
    print("=" * 50)

    examples = [1, 4, 7, 10, 49, 99, 1994, 2024, 3000]

    print("\nExamples:")
    for num in examples:
        roman = RomanNumeralConverter.to_roman(num)
        back = RomanNumeralConverter.from_roman(roman)
        print(f"  {num:4d} -> {roman:8s} -> {back}")

    print("\n" + "=" * 50)
    print()

    # Run tests
    run_all_tests()
