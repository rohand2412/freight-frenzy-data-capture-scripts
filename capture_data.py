#!/usr/bin/env python3
"""This script rapidly capture images and stores them for later labeling and usage as data"""

import cv2
from capture_data_utils import CaptureData

def main():
    """Main code"""
    CaptureData.InitBashArgs()
    args = CaptureData.InitBashArgs.get_args()

    img_dir = CaptureData.DirectoryManagement.WriteDir(target_dir=args.target_dir,
                                                       first_dir_name="Test0")
    img_dir.add()
    img_dir.debug(False)

    fps = CaptureData.Fps()

    frame = CaptureData.Frame(side=300, name="Cam", filename=args.filename, cameraId=2, limit_of_frames=args.limit_of_frames)

    try:
        while True:
            with fps.time_this():
                frame.capture_frame()
                frame.preprocessing()
                frame.imshow()
                frame.update()

                CaptureData.check_for_quit_request()

    except CaptureData.Break:
        frame.get_camera().release()
        cv2.destroyAllWindows()

        fps.calculate(frame.get_num())
        fps.debug(False)
        fps.print_fps()

        frame.export_buffer()

if __name__ == '__main__':
    main()
