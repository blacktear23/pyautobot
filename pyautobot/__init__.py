from .gui import alert, confirm, prompt, clip, snap, write, hotkey, paste, move, click, dclick, rclick, mdown, mup, scroll, click_and_paste, click_and_type
from .images import init_img, find_image_element, find_image_element2, click_image, click_image2, exists_image, exists_image2, wait_untile_exists, wait_untile_exists2
from .utils import wait, wait_input, os_name, is_windows, is_linux, is_macos
from .chrome import start_chrome, switch_to_tab, create_new_tab, list_tabs, scroll_page, snap_page, WINDOWS_UA, LINUX_UA, MACOS_UA, find_element, find_elements, get_parent
from .ocr import init_ocr, find_ocr_element


# Initialize
def init(screen_ratio=(1, 1), enable_ocr=False, ocr_langs=['en'], enable_gpu=False):
    init_img(screen_ratio)
    if enable_ocr:
        init_ocr(ocr_langs, enable_gpu)


# Browser
def chrome(profile_dir=None, socks5_proxy=None, proxy=None, size=(1266, 800), position=(0, 0), user_agent=None, mobile_emulation=None, timeout=None):
    return start_chrome(profile_dir, socks5_proxy, proxy, size, position, user_agent, mobile_emulation, timeout)


def switch_tab(driver, idx=None, name='', url='', mode='contains'):
    switch_to_tab(driver, idx, name, url, mode)


def new_tab(driver, url=''):
    create_new_tab(driver, url)


def tabs(driver):
    return list_tabs(driver)


def get_new_tabs(driver, origin_tabs):
    new_tabs = list_tabs(driver)
    if len(new_tabs) <= len(origin_tabs):
        return []

    origin_ids = [item.get('targetId', '') for item in origin_tabs]

    ret = []
    for tab in new_tabs:
        if tab['targetId'] not in origin_ids:
            ret.append(tab)
    return ret


def shell(local=None, banner='PyAutoBot Shell'):
    import code
    import importlib
    from selenium.webdriver.common.by import By
    # Setup rpa module
    spec = importlib.machinery.ModuleSpec('bot', None)
    mbot = importlib.util.module_from_spec(spec)
    for fn in __all__:
        setattr(mbot, fn, globals()[fn])

    # Default local should have rpa and By module
    local_obj = {'bot': mbot, 'By': By}
    if isinstance(local, dict):
        local_obj.update(local)
    code.interact(banner=banner, local=local_obj)


__all__ = [
    # Initialize functions
    'init', 'init_img', 'init_ocr',
    # OS Related functions
    'os_name', 'is_windows', 'is_linux', 'is_macos',
    # Wait and sleep functions
    'wait', 'wait_input', 'shell',
    # Prompt and dialog functions
    'alert', 'confirm', 'prompt',
    # Copy/paste and keyboard input
    'clip', 'write', 'hotkey', 'paste', 'click_and_paste', 'click_and_type',
    # Mouse control functions
    'move', 'click', 'dclick', 'rclick', 'mdown', 'mup', 'scroll',
    # Image find functions
    'find_image_element', 'find_image_element2',
    'click_image', 'click_image2',
    'exists_image', 'exists_image2',
    'wait_untile_exists', 'wait_untile_exists2',
    # Chrome related functions
    'chrome', 'switch_tab', 'new_tab', 'tabs', 'get_new_tabs', 'scroll_page',
    'WINDOWS_UA', 'LINUX_UA', 'MACOS_UA',
    'find_element', 'find_elements', 'get_parent',
    # Screen shot or browser screen shot
    'snap', 'snap_page',
    # OCR functions
    'find_ocr_element',
]
