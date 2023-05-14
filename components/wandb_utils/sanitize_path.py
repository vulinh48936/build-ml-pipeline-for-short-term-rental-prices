import os
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def sanitize_path(s):
    """
    Sanitizes the input path by:

    1. Expanding environment variables
    2. Expanding the home directory ('~')
    3. Calculating the absolute path

    :param s: input path
    :return: a sanitized version of the input path
    """
    return os.path.abspath(os.path.expanduser(os.path.expandvars(s)))
