import sys
# credit: https://codingdojo.org/

def number_to_numeral(number):
    """
    >>> number_to_numeral(1)
    'I'
    >>> number_to_numeral(2)
    'II'
    >>> number_to_numeral(12)
    'XII'
    >>> number_to_numeral(10)
    'X'
    >>> number_to_numeral(20)
    'XX'
    >>> number_to_numeral(99)
    'XCIX'
    >>> number_to_numeral(100)
    'C'
    >>> number_to_numeral(199)
    'CXCIX'
    >>> number_to_numeral(2399)
    'MMCCCXCIX'
    >>> number_to_numeral(4000)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range

    """

    numerals_dict = {
        'ones':     ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
        'tens':     ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
        'hundreds': ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'],
        'thousands': ['', 'M', 'MM', 'MMM'],
    }

    s = []
    # https://www.w3schools.com/python/python_for_loops.asp
    for index in ['ones', 'tens', 'hundreds', 'thousands']:
        # https://www.w3schools.com/python/ref_func_divmod.asp
        number, remainder = divmod(number, 10)
        s.insert(0, numerals_dict[index][remainder])
    return ''.join(s)

def main() -> int:
    """Echo the input arguments to standard output"""
    entered = input("enter a decimal number: ")
    print(number_to_numeral(int(entered)))
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit