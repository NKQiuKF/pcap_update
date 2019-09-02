import os


def check_sudo():
    """
    Checks for sudo/Administrator privileges
    """
    check = None
    if getattr(os, "geteuid"):
        check = os.geteuid() == 0

    return check
