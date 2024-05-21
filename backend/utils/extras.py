def has_duplicates(lst):
    return len(lst) != len(set(lst))

def is_fractional_part_zero(d):
    # Subtract the integer part from the decimal number
    fractional_part = d - int(d)
    return fractional_part == 0