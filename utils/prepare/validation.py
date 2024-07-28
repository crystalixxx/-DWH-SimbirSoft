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

    return all(isinstance(elem, int) for elem in column)


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
