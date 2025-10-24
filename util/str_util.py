import os
import pathlib


def myfunc(x: str) -> str:
    """
    Simple function

    Args:
        x (str): The input string

    Returns:
        str: The cleaned output string
    """    
    return x.strip()


def myfunc2() -> list:
    """
    Return me a simple list.

    Returns:
        list: The output list
    """    
    mylist = [1, 3]
    return mylist