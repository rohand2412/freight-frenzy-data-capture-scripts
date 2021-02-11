#!/usr/bin/env python3
"""This script contains all of the modules that are tied to the camera"""

import numpy as np
import cv2

class Packages:
    """Encapsulates all classes in this file in case inheritance of these classes is necessary"""

    class Frame:
        """Keeps track of all data regarding the video stream"""
        def __init__(self, name):
            self._width = 640
            self._height = 480
            self._camera = PiVideoStream(resolution=(self._width, self._height)).start()
            time.sleep(2.0)
            self._name = name
            self._frame = np.array([])

        def capture_frame(self):
            """Reads the frame from the video stream"""
            self._frame = self._camera.read()

        def preprocessing(self):
            """Preprocesses the frame"""

        def imshow(self):
            """Displays the frame"""
            cv2.imshow(self._name, self._frame)

        def update(self):
            """Checks certain break conditions and updates certain variables"""

        def get_name(self):
            """Returns name of the camera"""
            return self._name

        def get_camera(self):
            """Returns video stream object"""
            return self._camera

        def get_width(self):
            """Returns raw width of frame"""
            return self._width

        def get_height(self):
            """Returns raw height of frame"""
            return self._height