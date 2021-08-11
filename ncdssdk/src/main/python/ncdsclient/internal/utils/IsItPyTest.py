import os


def is_py_test():
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True
    return False
