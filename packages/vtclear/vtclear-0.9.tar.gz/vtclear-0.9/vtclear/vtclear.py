#!/usr/bin/env python3

"""
VT100 ASCII clear implemented in Python3.
http://www.termsys.demon.co.uk/vtansi.htm#erase
"""


def clear_screen() -> None:
    """
    Clear the screen.
    """
    print(f"{chr(27)}[2J{chr(27)}[H", end="")
