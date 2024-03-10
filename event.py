import cv2

def mouse_click(event, x, y, flags, param):
    global click_l
    if event == cv2.EVENT_FLAG_LBUTTON:
        click_l = True