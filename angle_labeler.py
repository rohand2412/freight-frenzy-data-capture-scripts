import os
import cv2
import pickle
import enum
import numpy as np
import pandas as pd
from raspberry_pi_libraries import multi_wrapper

LABELS_DIR = None
IMAGES_DIR = None
IMAGES_TOTAL_NUM = None
IMAGE_SIZE = None
IMAGE_NAMES = None

class State(enum.Enum):
    """Store state of labeler"""
    BROWSE = 0
    EDIT = 1

class Key:
    """Stores important key data"""
    def __init__(self, name, callback):
        self._name = name
        self._callback = callback
        self._state = multi_wrapper.Packages.KEYBOARD_RELEASED_STATE
        self._action_type = None
        self._tap_status = None

    def update(self, event):
        """Update data with latest event info"""
        if event.get_name() == self._name:
            self._state = event.get_state()
            self._action_type = event.get_action_type()

    def trigger_callback(self):
        """Update tap status and trigger callback"""
        if self._state == multi_wrapper.Packages.KEYBOARD_PRESSED_STATE:
            if self._action_type == multi_wrapper.Packages.KEYBOARD_ACTION_TYPE_TAP and not self._tap_status:
                self._callback()
                self._tap_status = True
            elif self._action_type == multi_wrapper.Packages.KEYBOARD_ACTION_TYPE_HOLD:
                self._callback()
        elif self._state == multi_wrapper.Packages.KEYBOARD_RELEASED_STATE:
            self._tap_status = False

    def set_state(self, new_state):
        """Set state"""
        self._state = new_state

    def set_action_type(self, new_action_type):
        """Set action type"""
        self._action_type = new_action_type

    def set_tap_status(self, new_tap_status):
        """Set status of tap"""
        self._tap_status = new_tap_status

    def get_state(self):
        """Access state"""
        return self._state

    def get_action_type(self):
        """Access action type"""
        return self._action_type

    def get_tap_status(self):
        """Access tap status"""
        return self._tap_status

    def get_name(self):
        """Return key event name"""
        return self._name

image_num = 0
state = State.BROWSE
labels = None

def left_key_callback():
    """Executes upon press of left key"""
    global image_num, state, IMAGE_NAMES, labels
    if state == State.BROWSE and image_num > 0:
        image_num -= 1
    elif state == State.EDIT and labels.loc[IMAGE_NAMES[image_num], "x"] > 0:
        labels.loc[IMAGE_NAMES[image_num], "x"] -= 1

def right_key_callback():
    """Executes upon press of right key"""
    global image_num, state, IMAGES_TOTAL_NUM, IMAGE_NAMES, labels
    if state == State.BROWSE and image_num < IMAGES_TOTAL_NUM - 1:
        image_num += 1
    elif state == State.EDIT and labels.loc[IMAGE_NAMES[image_num], "x"] < IMAGE_SIZE - 1:
        labels.loc[IMAGE_NAMES[image_num], "x"] += 1

def up_key_callback():
    """Executes upon press of up key"""
    global image_num, state, IMAGE_NAMES, labels
    if state == State.EDIT and labels.loc[IMAGE_NAMES[image_num], "y"] > 0:
        labels.loc[IMAGE_NAMES[image_num], "y"] -= 1

def down_key_callback():
    """Executes upon press of down key"""
    global image_num, state, IMAGE_NAMES, labels
    if state == State.EDIT and labels.loc[IMAGE_NAMES[image_num], "y"] < IMAGE_SIZE - 1:
        labels.loc[IMAGE_NAMES[image_num], "y"] += 1

def enter_key_callback():
    """Executes upon press of enter key"""
    global image_num, state, IMAGE_NAMES, labels
    if state == State.BROWSE:
        state = State.EDIT
        labels.loc[IMAGE_NAMES[image_num], "labeled"] = True
    elif state == State.EDIT:
        state = State.BROWSE

def main():
    """Main code"""
    global image_num, state, labels, LABELS_DIR, IMAGES_DIR, \
           IMAGES_TOTAL_NUM, IMAGE_SIZE, IMAGE_NAMES

    LABELS_DIR = ""
    IMAGES_DIR = "/home/rohan/Documents/RCJ2021Repos/raspberry-pi-images-rcj/Evac-Subset-300/Final-Images/"

    keyboard = multi_wrapper.Packages.Keyboard()
    keyboard.start()

    IMAGE_NAMES = multi_wrapper.Packages.Dataset.get_ordered_path(IMAGES_DIR)
    image_file_ext = os.path.splitext(os.listdir(IMAGES_DIR)[0])[1]

    images = {}
    for i, _ in enumerate(IMAGE_NAMES):
        IMAGE_NAMES[i] = os.path.splitext(IMAGE_NAMES[i])[0]
        images[IMAGE_NAMES[i]] = cv2.imread(IMAGES_DIR + IMAGE_NAMES[i] + image_file_ext)

    IMAGES_TOTAL_NUM = len(images)
    IMAGE_SIZE = images[IMAGE_NAMES[0]].shape[0]

    labels = pd.DataFrame([0 for i, _ in enumerate(IMAGE_NAMES)], columns=["angle"])
    labels = labels.assign(x=[IMAGE_SIZE // 2 for i, _ in enumerate(IMAGE_NAMES)])
    labels = labels.assign(y=[0 for i, _ in enumerate(IMAGE_NAMES)])
    labels = labels.assign(labeled=[False for i, _ in enumerate(IMAGE_NAMES)])
    labels.index = IMAGE_NAMES

    left_key = Key("left", left_key_callback)
    right_key = Key("right", right_key_callback)
    up_key = Key("up", up_key_callback)
    down_key = Key("down", down_key_callback)
    enter_key = Key("enter", enter_key_callback)
    a_key = Key("a", left_key_callback)
    d_key = Key("d", right_key_callback)
    w_key = Key("w", up_key_callback)
    s_key = Key("s", down_key_callback)
    space_key = Key("space", enter_key_callback)

    ROBOT = {"x": IMAGE_SIZE//2, "y": IMAGE_SIZE - 1}

    try:
        while True:
            while not keyboard.get_events().empty():
                event = keyboard.get_events().get()
                print(event.get_name())
                left_key.update(event)
                right_key.update(event)
                up_key.update(event)
                down_key.update(event)
                enter_key.update(event)
                a_key.update(event)
                d_key.update(event)
                w_key.update(event)
                s_key.update(event)
                space_key.update(event)

            left_key.trigger_callback()
            right_key.trigger_callback()
            up_key.trigger_callback()
            down_key.trigger_callback()
            enter_key.trigger_callback()
            a_key.trigger_callback()
            d_key.trigger_callback()
            w_key.trigger_callback()
            s_key.trigger_callback()
            space_key.trigger_callback()

            if labels.loc[IMAGE_NAMES[image_num], "labeled"]:
                image_draw = cv2.circle(images[IMAGE_NAMES[image_num]].copy(),
                                        (labels.loc[IMAGE_NAMES[image_num], "x"],
                                        labels.loc[IMAGE_NAMES[image_num], "y"]),
                                        radius=2, color=(0, 255, 0), thickness=-1)
                image_draw = cv2.line(image_draw,
                                    (labels.loc[IMAGE_NAMES[image_num], "x"],
                                    labels.loc[IMAGE_NAMES[image_num], "y"]),
                                    (ROBOT["x"], ROBOT["y"]),
                                    color=(0, 255, 0), thickness=1)

                cv2.imshow("image", cv2.resize(image_draw, (IMAGE_SIZE * 2, IMAGE_SIZE * 2)))

            else:
                cv2.imshow("image", cv2.resize(images[IMAGE_NAMES[image_num]],
                                               (IMAGE_SIZE* 2, IMAGE_SIZE* 2)))

            multi_wrapper.Packages.check_for_quit_request()

    except multi_wrapper.Packages.Break:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
