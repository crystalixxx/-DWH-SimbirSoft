def can_be_nullable(column):
    return any(isinstance(elem, str) and len(elem) == 0 for elem in column)


def is_unique_column(column):
    values = set()

    for elem in column:
        if elem not in values:
            values.add(elem)
        else:
            return False

    return True


def is_bool_column(column):
    return all(elem in (0, 1) for elem in column)


def is_int_column(column):
    if is_bool_column(column):
        return False

    min_int_value = -2147483648
    max_int_value = 2147483647

    return all(isinstance(elem, int) and min_int_value <= elem <= max_int_value for elem in column)


def is_bigint_column(column):
    if is_bool_column(column) or is_float_column(column):
        return False

    min_bigint_value = -9223372036854775808
    max_bigint_value = 9223372036854775807

    return all(isinstance(elem, int) and min_bigint_value <= elem <= max_bigint_value for elem in column)


def is_float_column(column):
    if is_int_column(column):
        return False

    return any(isinstance(elem, float) for elem in column)


def is_datetime_column(column):
    if is_int_column(column) or is_float_column(column):
        return False

    return all(isinstance(elem, str) and len(elem.split('-')) >= 2 for elem in column)


def is_str_column(column):
    if is_datetime_column(column):
        return False

    return True


def is_json_column(column):
    return all(isinstance(elem, dict) for elem in column)
