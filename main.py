import time
import threading

from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

TOOGLE_KEY = KeyCode(char="-")

clicking = False
mouse = Controller()

def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
        time.sleep(0.0001)


def toggle_event(key):
    if key == TOOGLE_KEY:
        global clicking
        clicking = not clicking
        print(f'autoclicker : {clicking}')


click_thread = threading.Thread(target=clicker)
click_thread.start()

with Listener(on_press=toggle_event) as listener:
    listener.join()