from uuid import UUID


def check_that_string_is_uuid(u):
    if len(u) != 36:
        return False

    try:
        UUID(u)
        return True
    except ValueError:
        return False
