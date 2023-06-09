import time
import platform


def wait(sec=1):
    time.sleep(sec)


def wait_input(prompt='Input: '):
    return input(prompt)


def os_name():
    return platform.system()


def is_windows():
    return os_name() == 'Windows'


def is_linux():
    return os_name() == 'Linux'


def is_macos():
    return os_name() == 'Darwin'
