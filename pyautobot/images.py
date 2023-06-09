import cv2
import pyautogui
import numpy as np
from .gui import move, click, paste
from .utils import wait


SCREEN_HRATIO = 1
SCREEN_WRATIO = 1
THRESHOLD = 0.8
ELEMENT_IMAGE_RATIO = (1, 1)


def init_img(element_ratio=None):
    global SCREEN_HRATIO
    global SCREEN_WRATIO
    global ELEMENT_IMAGE_RATIO
    img = pyautogui.screenshot()
    w, h = img.size
    ss = pyautogui.size()
    SCREEN_HRATIO = h / ss.height
    SCREEN_WRATIO = w / ss.width
    if element_ratio is not None:
        ELEMENT_IMAGE_RATIO = element_ratio
    print('Screen Ratio: %s, %s' % (SCREEN_WRATIO, SCREEN_HRATIO))
    print('Elememt Image Ratio: %s, %s' % ELEMENT_IMAGE_RATIO)


# Scale image to new ratio
def scale_image(img, ratio):
    xr, yr = ratio[0], ratio[1]
    if xr == 1 and yr == 1:
        return img

    shape = img.shape
    if len(shape) < 2:
        return img

    h, w = shape[0], shape[1]
    nw = int(w * xr)
    nh = int(h * yr)
    op = cv2.INTER_LINEAR
    if nw < xr and nh < yr:
        # Shrink better
        op = cv2.INTER_AREA
    return cv2.resize(img, (nw, nh), interpolation=op)


def __global_scale_image(img):
    return scale_image(img, ELEMENT_IMAGE_RATIO)


def find_image_element(element, pmode='center', debug=False, threshold=None):
    elem_img = __global_scale_image(cv2.imread(element))
    h, w, _ = elem_img.shape
    pil_screen_img = pyautogui.screenshot()
    screen_img = cv2.cvtColor(np.array(pil_screen_img), cv2.COLOR_RGB2BGR)

    src_img_g = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    elem_img_g = cv2.cvtColor(elem_img, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(src_img_g, elem_img_g, cv2.TM_CCOEFF_NORMED)
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)
    x, y = max_loc[0], max_loc[1]

    if debug:
        print('DEBUG: x = %s, y = %s, max_val = %s' % (x, y, max_val))
        # Draw element rectangle
        cv2.rectangle(screen_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imwrite('debug.png', screen_img)

    if threshold is None:
        threshold = THRESHOLD

    if max_val <= threshold:
        return False, 0, 0

    if pmode == 'center':
        x = x / SCREEN_WRATIO + w / 2 / SCREEN_WRATIO
        y = y / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO
    elif pmode == 'topleft':
        x = x / SCREEN_WRATIO
        y = y / SCREEN_HRATIO
    elif pmode == 'topright':
        x = x / SCREEN_WRATIO + w / SCREEN_WRATIO
        y = y / SCREEN_HRATIO
    elif pmode == 'centerleft':
        x = x / SCREEN_WRATIO
        y = y / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO
    elif pmode == 'centerright':
        x = x / SCREEN_WRATIO + w / SCREEN_WRATIO
        y = y / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO

    return True, int(x), int(y)


def find_image_element2(location, element, pmode='center', debug=False, threshold=None):
    location_img = __global_scale_image(cv2.imread(location))
    lh, lw, _ = location_img.shape
    pil_screen_img = pyautogui.screenshot()
    screen_img = cv2.cvtColor(np.array(pil_screen_img), cv2.COLOR_RGB2BGR)

    src_img_g = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    loc_img_g = cv2.cvtColor(location_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(src_img_g, loc_img_g, cv2.TM_CCOEFF_NORMED)
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)

    if debug:
        print('DEBUG: x = %s, y = %s, max_val = %s' % (max_loc[0], max_loc[1], max_val))

    if threshold is None:
        threshold = THRESHOLD

    if max_val <= threshold:
        return False, 0, 0

    loc_x, loc_y = max_loc[0], max_loc[1]
    elem_img = __global_scale_image(cv2.imread(element))
    h, w, _ = elem_img.shape
    elem_img_g = cv2.cvtColor(elem_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(loc_img_g, elem_img_g, cv2.TM_CCOEFF_NORMED)
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)

    x, y = max_loc[0], max_loc[1]
    x += loc_x
    y += loc_y
    if debug:
        print('DEBUG: x = %s, y = %s, max_val = %s' % (x, y, max_val))
        # Draw location rectangle
        cv2.rectangle(screen_img, (loc_x, loc_y), (loc_x + lw, loc_y + lh), (0, 0, 255), 2)
        # Draw element rectangle
        cv2.rectangle(screen_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imwrite('debug.png', screen_img)

    if max_val <= threshold:
        return False, 0, 0

    if pmode == 'center':
        x = x / SCREEN_WRATIO + w / 2 / SCREEN_WRATIO
        y = y / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO
    elif pmode == 'topleft':
        x = x / SCREEN_WRATIO
        y = y / SCREEN_HRATIO
    elif pmode == 'topright':
        x = x / SCREEN_WRATIO + w / SCREEN_WRATIO
        y = y / SCREEN_HRATIO
    elif pmode == 'centerleft':
        x = x / SCREEN_WRATIO
        y = y / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO
    elif pmode == 'centerright':
        x = x / SCREEN_WRATIO + w / SCREEN_WRATIO
        y = y / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO

    return True, int(x), int(y)


def click_image(elem, debug=False, threshold=None):
    found, x, y = find_image_element(elem, debug=debug, threshold=threshold)
    if not found:
        return

    move(x, y)
    click()


def click_image2(location, elem, debug=False, threshold=None):
    found, x, y = find_image_element2(location, elem, debug=debug, threshold=threshold)
    if not found:
        return
    move(x, y)
    click()


def exists_image(elem, debug=False, threshold=None):
    found, _, _ = find_image_element(elem, debug=debug, threshold=threshold)
    return found


def exists_image2(location, elem, debug=False, threshold=None):
    found, _, _ = find_image_element2(location, elem, debug=debug, threshold=threshold)
    return found


def wait_untile_exists(elem, next_op=None, max_wait=20, duration=1, debug=False, threshold=None):
    found = False
    for i in range(max_wait):
        found, x, y = find_image_element(elem, debug=debug, threshold=threshold)
        if found:
            break
        wait(duration)

    if found:
        if next_op == 'click':
            move(x, y)
            click()
        elif next_op == 'hover':
            move(x, y)
        elif next_op == 'click_paste':
            move(x, y)
            click()
            paste()
        return x, y
    return None, None


def wait_untile_exists2(location, elem, next_op=None, max_wait=20, duration=1, debug=False, threshold=None):
    found = False
    for i in range(max_wait):
        found, x, y = find_image_element2(location, elem, debug=debug, threshold=threshold)
        if found:
            break
        wait(duration)

    if found:
        if next_op == 'click':
            move(x, y)
            click()
        elif next_op == 'hover':
            move(x, y)
        elif next_op == 'click_paste':
            move(x, y)
            click()
            paste()
        return x, y
    return None, None
