import cv2
import pyautogui
import numpy as np


EASYOCR_READER = None


def init_ocr(langs=['en'], enable_gpu=False):
    import easyocr
    global EASYOCR_READER
    EASYOCR_READER = easyocr.Reader(langs, gpu=enable_gpu)


def compare_text(text, rtext):
    if text in rtext:
        return True
    elif text.replace(' ', '') in rtext.replace(' ', ''):
        return True
    return False


def find_ocr_element(text, pmode='center', rect=None, debug=True, threshold=None):
    from .images import THRESHOLD, SCREEN_HRATIO, SCREEN_WRATIO
    print(SCREEN_HRATIO, SCREEN_WRATIO)
    if EASYOCR_READER is None:
        print('Alert: OCR system not initialized')
        return False, 0, 0

    if threshold is None:
        threshold = THRESHOLD

    pil_screen_img = pyautogui.screenshot()
    screen_np = np.array(pil_screen_img)
    screen_img = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    offset_x, offset_y = 0, 0
    if rect is not None and len(rect) == 4:
        x, y, w, h = rect
        offset_x = x
        offset_y = y
        cropped = screen_np[y:y + h, x:x + w]
        result = EASYOCR_READER.readtext(cropped)
    else:
        result = EASYOCR_READER.readtext(screen_np)
    founds = []
    confi_max = 0
    found_max = None
    for line in result:
        box, rtext, confi = line[0], line[1], line[2]
        if len(box) < 4 or confi < threshold:
            continue

        if compare_text(text, rtext):
            x, y = box[0][0], box[0][1]
            x2, y2 = box[-2][0], box[-2][1]
            w = int(x2 - x)
            h = int(y2 - y)
            item = [(int(x), int(y), w, h), rtext, confi]
            founds.append(item)
            if confi > confi_max:
                confi_max = confi
                found_max = item

    if debug:
        for f in founds:
            x, y, w, h = f[0]
            print('DEBUG: x = %s, y = %s, confidence = %s, text = %s' % (x, y, f[2], f[1]))
            cv2.rectangle(screen_img, (x + offset_x, y + offset_y), (x + w + offset_x, y + h + offset_y), (0, 0, 255), 2)
            cv2.imwrite('debug.png', screen_img)

    if found_max is None:
        return False, 0, 0

    x, y, w, h = found_max[0]
    if pmode == 'center':
        x = (x + offset_x) / SCREEN_WRATIO + w / 2 / SCREEN_WRATIO
        y = (y + offset_y) / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO
    elif pmode == 'topleft':
        x = (x + offset_x) / SCREEN_WRATIO
        y = (y + offset_y) / SCREEN_HRATIO
    elif pmode == 'centerleft':
        x = (x + offset_x) / SCREEN_WRATIO
        y = (y + offset_y) / SCREEN_HRATIO + h / 2 / SCREEN_HRATIO

    return True, int(x), int(y)
