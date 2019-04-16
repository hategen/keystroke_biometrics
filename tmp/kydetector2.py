import time

# import pandas as pd
import numpy as np
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pandas as pd
controller = Controller()

keyAssignature = []
interval = None
dwell = None
latency = None
flight = None
up2up = None
originPassword = 'rabbit-123'
enteredPassword = ''
shiftPressed = False

try:
    df = pd.DataFrame.read_csv('assignature.csv')
except:
    df = pd.DataFrame()


def on_release(key):  # what to do on key-release
    # converting float to str, slicing the float
    global interval, dwell, latency, flight, up2up, keyAssignature, enteredPassword, shiftPressed, df
    # ti1 = str(time.time() - t)[0:5]
    # print("The key", key, " is pressed for", ti1, 'seconds')
    if (key is keyboard.Key.shift_r) or (key is keyboard.Key.shift_l):
        shiftPressed = False
        pass
    elif key == keyboard.Key.enter:
        # Stop listener
        print('compare', originPassword, enteredPassword)
        if (originPassword == enteredPassword):
            print('pass is valid')
            df = df.append([[keyAssignature]])
            df.to_csv('assignature.csv')
        keyAssignature = []
        interval = None
        dwell = None
        latency = None
        flight = None
        up2up = None
        enteredPassword = ''
    else:
        if (shiftPressed):
            print('shift pressed')

        enteredPassword += key.char
        # print(chr(ord(key.char)-32))
        if not up2up is None:
            keyAssignature.append(round(time.time() - up2up, 3))
        if (not up2up is None) and (not dwell is None):
            keyAssignature.append(round(2 * time.time() - dwell - up2up, 3))
        if not dwell is None:
            keyAssignature.append(round(time.time() - dwell, 3))
        

        interval = time.time()
        up2up = time.time()

def on_press(key):  # what to do on key-press
    global interval, dwell, latency, flight, up2up, keyAssignature, shiftPressed
    if (key is keyboard.Key.shift_r) or (key is keyboard.Key.shift_l):
        shiftPressed = True
        pass
    elif key == keyboard.Key.enter:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        try:
            if not flight is None:
                keyAssignature.append(round(time.time() - flight, 3))
            if not interval is None:
                keyAssignature.append(round(time.time() - interval, 3))
            dwell = time.time()
            flight = time.time()
            interval = time.time()

        except AttributeError:
            print('special key {0} pressed'.format(
                key))


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# dwell, flight, interval, up2up, latency, dwell,....
