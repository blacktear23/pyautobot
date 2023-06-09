import time
import platform
import pyautogui
import pyperclip


# message box
def alert(text, title='Alert'):
    pyautogui.alert(text=text, title=title, button='OK')


def confirm(text, title='Confirm'):
    ret = pyautogui.confirm(text=text, title=title, buttons=['OK', 'Cancel'])
    return ret == 'OK'


def prompt(text, title='Please Input', default=''):
    ret = pyautogui.prompt(text, title, default)
    return ret


# clipboard and keyboard control
def clip(text):
    pyperclip.copy(text)


def snap(fname=None):
    if fname is None:
        return pyautogui.screenshot()
    return pyautogui.screenshot(fname)


def write(text, interval=0.4):
    pyautogui.write(text, interval=interval)


def hotkey(*args):
    pyautogui.hotkey(*args)
    time.sleep(0.4)


def paste(text=None):
    if text is not None:
        pyperclip.copy(text)
    if platform.system() == 'Darwin':
        hotkey('command', 'v')
    else:
        hotkey('ctrl', 'v')


# Mouse control
def move(x, y):
    pyautogui.moveTo(x, y, duration=0.2)


def click(x=None, y=None, clicks=1):
    if x is not None and y is not None:
        move(x, y)
    pyautogui.click(clicks=clicks)


def dclick(x=None, y=None):
    click(x, y, 2)


def rclick(x=None, y=None, clicks=1):
    if x is not None and y is not None:
        move(x, y)
    pyautogui.click(button='right', clicks=clicks)


def mdown(x=None, y=None):
    if x is not None and y is not None:
        move(x, y)
    pyautogui.mouseDown()


def mup(x=None, y=None):
    if x is not None and y is not None:
        move(x, y)
    pyautogui.mouseUp()


def scroll(steps):
    pyautogui.scroll(steps)


def click_and_paste(x, y, text):
    clip(text)
    move(x, y)
    click()
    paste()


def click_and_type(x, y, text, interval=0.2):
    move(x, y)
    click()
    write(text, interval)
