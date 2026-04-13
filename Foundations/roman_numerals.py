def int_to_roman(num):
    if not (0 < num < 3000):
        raise ValueError("Number must be between 1 and 2999")

    val = [
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

    roman_numeral = ""
    for integer, numeral in val:
        while num >= integer:
            roman_numeral += numeral
            num -= integer
    return roman_numeral


print(int_to_roman(1994))  # Output: MCMXCIV
