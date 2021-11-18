import cv2

cam = cv2.VideoCapture(2)

while cam.isOpened():
    check, frame = cam.read()

    if check:
        cv2.imshow('video', frame)

    if chr(cv2.waitKey(1)&255) == 'q':
        break

cam.release()
cv2.destroyAllWindows()