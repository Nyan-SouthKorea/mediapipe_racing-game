import pyautogui
from state import State
import time

def joystick():
    if State.go_state:
        State.miss_cnt = 0
    else:
        State.miss_cnt += 1

    if State.miss_cnt >= 3:
        print('brake')
        if not State.drift_state:
            State.drift_state = True
            pyautogui.keyDown('down')

        # if State.left_state:
        #     State.left_state = False
        #     pyautogui.keyUp('left')

        # if State.right_state:
        #     State.right_state = False
        #     pyautogui.keyUp('right')

    else:
        if State.new_button_state and State.go_state:
            print('bosster')
            pyautogui.keyDown('space')
            time.sleep(0.1)
            pyautogui.keyUp('space')

        if State.drift_state:
            State.drift_state = False
            pyautogui.keyUp('down')
        
    if State.move == 'Left':
        if not State.left_state:
            State.left_state = True
            pyautogui.keyDown('left')
        
        if State.right_state:
            State.right_state = False
            pyautogui.keyUp('right')

    elif State.move == 'Right':
        if not State.right_state:
            State.right_state = True
            pyautogui.keyDown('right')
        
        if State.left_state:
            State.left_state = False
            pyautogui.keyUp('left')

    else:
        if State.right_state:
            State.right_state = False
            pyautogui.keyUp('right')

        if State.left_state:
            State.left_state = False
            pyautogui.keyUp('left')
