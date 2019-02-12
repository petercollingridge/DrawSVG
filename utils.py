from math import floor, ceil, log10


def get_tick_size(start_value, end_value, max_divisions, min_unit=0):
    unit_value = max(min_unit, pow(10, floor(log10(end_value - start_value) - 1)))
    max_value = abs(end_value)

    #  Increase unit value only using nice numbers
    if unit_value < max_value / 20:
        unit_value *= 2
    if unit_value < max_value / 16:
        unit_value *= 1.25

    while unit_value < max_value / max_divisions:
        unit_value *= 2

    start_value = floor(start_value / unit_value) * unit_value
    end_value = ceil(end_value / unit_value) * unit_value

    return unit_value, start_value, end_value


def get_max_divisions(position_1, position_2):
    return max(2, floor(abs(position_2 - position_1) / 25))
