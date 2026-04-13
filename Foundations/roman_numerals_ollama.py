import re


def int_to_roman(num):
    """
    Convert an integer to a Roman numeral.
    Args:
        num (int): Integer between 1 and 3000
    Returns:
        str: Roman numeral representation

    Examples:
        >>> int_to_roman(1)
        'I'
        >>> int_to_roman(10)
        'X'
        >>> int_to_roman(7)
        'VII'
    """
    if not isinstance(num, int) or num <= 0 or num > 3000:
        raise ValueError("Input must be an integer between 1 and 3000")

    # Define mapping of values to Roman numerals in descending order
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

    result = []

    # Process each value from largest to smallest
    for i in range(len(values)):
        # Add the numeral as many times as the value fits into num
        count = num // values[i]
        if count > 0:
            result.append(numerals[i] * count)
            num -= values[i] * count

    return "".join(result)


_ROMAN_PATTERN = re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")


def roman_to_int(roman):
    """
    Convert a Roman numeral to an integer.

    Args:
        roman (str): Roman numeral string

    Returns:
        int: Integer representation

    Examples:
        >>> roman_to_int('I')
        1
        >>> roman_to_int('X')
        10
        >>> roman_to_int('VII')
        7
    """
    if not isinstance(roman, str):
        raise ValueError("Input must be a string")

    roman = roman.strip().upper()
    if not roman:
        raise ValueError("Roman numeral cannot be empty")

    if not _ROMAN_PATTERN.match(roman):
        raise ValueError("Invalid Roman numeral format")

    # Define mapping of Roman numerals to values
    roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    total = 0
    prev_value = 0

    # Process from right to left
    for char in reversed(roman):
        if char not in roman_values:
            raise ValueError(f"Invalid Roman numeral character: {char}")

        current_value = roman_values[char]

        # If current value is less than previous, subtract it (for cases like IV, IX)
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value

        prev_value = current_value

    return total


# Test cases for verification
if __name__ == "__main__":
    # Test int_to_roman
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
        (20, "XX"),
        (30, "XXX"),
        (40, "XL"),
        (50, "L"),
        (60, "LX"),
        (70, "LXX"),
        (80, "LXXX"),
        (90, "XC"),
        (100, "C"),
        (200, "CC"),
        (300, "CCC"),
        (400, "CD"),
        (500, "D"),
        (600, "DC"),
        (700, "DCC"),
        (800, "DCCC"),
        (900, "CM"),
        (1000, "M"),
        (1994, "MCMXCIV"),
        (3000, "MMM"),
    ]

    print("Testing int_to_roman:")
    for num, expected in test_cases:
        result = int_to_roman(num)
        print(f"{num} -> {result} {'✓' if result == expected else '✗'}")

    print("\nTesting roman_to_int:")
    for expected, roman in test_cases:
        result = roman_to_int(roman)
        print(f"{roman} -> {result} {'✓' if result == expected else '✗'}")

    # Test reverse conversion
    print("\nTesting reverse conversion:")
    for num, _roman in test_cases:
        converted_back = roman_to_int(int_to_roman(num))
        print(
            f"{num} -> {int_to_roman(num)} -> {converted_back} "
            f"{'✓' if converted_back == num else '✗'}"
        )
