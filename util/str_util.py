import os
import pathlib


def myfunc(x: str) -> str:
    return x.strip()


def myfunc2() -> list:
    """
    Return me a simple list.

    Returns:
        list: The output list
    """    
    mylist = [1, 2, 3]
    return mylist