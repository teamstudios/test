import base64


def convert_str_to_float(string):
    """
    Try convert string to float. If exception then return 0.0.
    :param string: string to convert
    :return: float
    """
    try:
        num = float(string)
    except ValueError:
        num = 0.0
    return num


def convert_str_to_int(string):
    """
    Try convert string to int. If exception then return 0.
    :param string: string to convert
    :return: int
    """
    try:
        num = int(string)
    except ValueError:
        num = 0
    return num


def base64_decode(s):
    """
    Add missing padding to string and return the decoded base64 string.
    """
    s = str(s).strip()
    try:
        return base64.b64decode(s)
    except Exception:
        padding = len(s) % 4
        if padding == 1:
            return ''
        elif padding == 2:
            s += '=='
        elif padding == 3:
            s += '='
        return base64.b64decode(s)