from sys import platform
from subprocess import call


def clear():
    if 'win' not in platform:
        cmd = 'clear'
    else:
        cmd = 'cls'
    try:
        call(cmd, shell=True)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    clear()
