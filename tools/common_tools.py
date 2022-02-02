def get_numbers_in_string(str_value, delimiter):
    if delimiter is None:
        return [float(s) for s in str_value if is_float(s)]
    else:
        return [float(s) for s in str_value.split(delimiter) if is_float(s)]


def get_first_number_in_string(str_value, delimiter):
    numbers = get_numbers_in_string(str_value, delimiter)
    if len(numbers) > 0:
        return numbers[0]
    else:
        return None


def is_float(str_value):
    try:
        float(str_value)
        return True
    except ValueError:
        return False
    except OverflowError:
        return False

