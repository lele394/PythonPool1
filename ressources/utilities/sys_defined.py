import os
import platform


def clear_screen():
    system_platform = platform.system()

    if system_platform == 'Windows':
        os.system('cls')
    else:
        os.system('clear')