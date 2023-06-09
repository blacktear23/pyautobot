import getpass
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By


BROWSER_OPERATION_TIMEOUT = 60


WINDOWS_UA = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'disable_ch': True,
    'platform': 'Windows',
    'mobile': False,
}

LINUX_UA = {
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'disable_ch': True,
    'platform': 'Linux',
    'mobile': False,
}

MACOS_UA = {
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'disable_ch': True,
    'platform': 'macOS',
    'mobile': False,
}


def start_chrome(profile_dir=None, socks5_proxy=None, proxy=None, size=(1366, 768), position=(0, 0), user_agent=None, mobile_emulation=None, timeout=None):
    if timeout is None:
        webdriver.remote.remote_connection.RemoteConnection.set_timeout(BROWSER_OPERATION_TIMEOUT)
    else:
        webdriver.remote.remote_connection.RemoteConnection.set_timeout(timeout)

    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('excludeSwitches', [
        'enable-automation',
        'disable-background-networking',
        'disable-default-apps',
        'disable-hang-monitor',
        'enable-blink-features',
        'no-service-autorun',
        'test-type',
        'use-mock-keychain',
    ])
    # Disable remember password feature
    opt.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
    })
    # Disable browser notification
    opt.add_argument('--disable-notifications')
    # Disable default browser check and confirm
    opt.add_argument('--no-default-browser-check')
    # Disable auto update check
    opt.add_argument("--simulate-outdated-no-au='Tue, 31 Dec 2099 23:59:59 GMT'")
    # If in linux and user is root just add --no-sandbox
    if platform.system() == 'Linux' and getpass.getuser() == 'root':
        opt.add_argument('--no-sandbox')

    if mobile_emulation is not None:
        user_agent = None
        opt.add_experimental_option("mobileEmulation", mobile_emulation)

    # user_agent is string, set user agent as chrome parameter and disable SEC-CH-UA
    if user_agent is not None:
        if isinstance(user_agent, str):
            opt.add_argument('--user-agent=%s' % user_agent)
            opt.add_argument('--disable-features=UserAgentClientHint')
        elif isinstance(user_agent, dict):
            opt.add_argument('--user-agent=%s' % user_agent['user_agent'])
            if user_agent.get('disable_ch', False):
                opt.add_argument('--disable-features=UserAgentClientHint')
    if position is not None:
        opt.add_argument('--window-position=%s,%s' % (position[0], position[1]))
    if size is not None:
        opt.add_argument('--window-size=%s,%s' % (size[0], size[1]))
    if profile_dir is not None:
        opt.add_argument('--user-data-dir=%s' % profile_dir)
    if socks5_proxy is not None:
        opt.add_argument('--proxy-server=socks5://%s' % socks5_proxy)
    if proxy is not None:
        opt.add_argument('--proxy-server=%s' % proxy)
    c = webdriver.Chrome(options=opt)
    # user_agent is dict, set user agent and SEC-CH-UA via CDP request
    if user_agent is not None and isinstance(user_agent, dict):
        if not user_agent.get('disable_ch', False):
            c.execute_cdp_cmd("Emulation.setUserAgentOverride", {
                'userAgent': user_agent['user_agent'],
                'platform': user_agent.get('platform', 'Windows'),
                'userAgentMetadata': {
                    'platform': user_agent.get('platform', 'Windows'),
                    'platformVersion': user_agent.get('version', ''),
                    'architecture': user_agent.get('architecture', ''),
                    'model': user_agent.get('model', ''),
                    'mobile': user_agent.get('mobile', False),
                },
            })
    return c


def get(b, url):
    b.get(url)


def __check(src, dst, mode):
    print(src, dst, mode)
    if mode == 'contains':
        return dst in src
    elif mode == 'equals':
        return dst == src
    return False


# Switch to browser tab
# mode: contains, equals
def switch_to_tab(driver, idx=None, name='', url='', mode='contains'):
    hdls = driver.window_handles
    try:
        current_hdl = driver.current_window_handle
    except Exception:
        current_hdl = hdls[0]

    if idx is not None:
        if idx >= len(hdls):
            return
        driver.switch_to.window(hdls[idx])

    found = False
    if name != '':
        for hdl in hdls:
            driver.switch_to.window(hdl)
            if __check(driver.title, name, mode):
                found = True
                break

        if not found:
            driver.switch_to.window(current_hdl)
        return

    if url != '':
        for hdl in hdls:
            driver.switch_to.window(hdl)
            if __check(driver.current_url, url, mode):
                found = True
                break

        if not found:
            driver.switch_to.window(current_hdl)
        return


def scroll_page(driver, steps):
    driver.execute_script("window.scrollTo(0, window.scrollY + %d)" % int(steps))


def create_new_tab(driver, url=''):
    driver.switch_to.new_window('tab')
    if url != '':
        driver.get(url)


def list_tabs(driver):
    ret = []
    data = driver.execute_cdp_cmd('Target.getTargets', {})
    targets = data.get('targetInfos', [])
    for handle in driver.window_handles:
        for tgt in targets:
            if tgt.get('targetId', '') == handle:
                ret.append(tgt)
    return ret


def snap_page(driver, fname=None):
    if fname is None:
        return driver.get_screenshot_as_png()
    return driver.get_screenshot_as_file(fname)


def get_parent(elem):
    return elem.find_element(By.XPATH, 'parent::*')


def __transform_by(kwargs):
    if len(kwargs) != 1:
        raise Exception('Invalid query argument, require only one query')

    by, query = list(kwargs.items())[0]
    if by.lower() == 'id':
        by = By.ID
    elif by.lower() == 'tag':
        by = By.TAG_NAME
    elif by.lower() == 'style':
        by = By.CLASS_NAME
    elif by.lower() == 'css':
        by = By.CSS_SELECTOR
    elif by.lower() == 'name':
        by = By.NAME
    elif by.lower() == 'xpath':
        by = By.XPATH
    else:
        raise Exception('Invalid query type: %s' % by)

    return by, query


def find_element(driver, **kwargs):
    by, query = __transform_by(kwargs)
    elems = driver.find_elements(by, query)
    if len(elems) == 0:
        return None
    return elems[0]


def find_elements(driver, **kwargs):
    by, query = __transform_by(kwargs)
    return driver.find_elements(by, query)
