import cv2 as cv
import numpy as np

import lanes


video = cv.VideoCapture('road.mp4')
if not video.isOpened():
    print('error while opening the video')

cv.waitKey(2)

while video.isOpened():
    _, frame = video.read()
    copy_frame = np.copy(frame)

    try:
        frame = lanes.canny(frame)
        frame = lanes.mask(frame)
        lines = cv.HoughLinesP(frame, 10, np.pi/180, 50, np.array([()]), minLineLength=20, maxLineGap=5)
        averaged_lines = lanes.average_slope_intercept(frame, lines)

        line_image = lanes.display_lines(copy_frame, averaged_lines)

        combo = cv.addWeighted(copy_frame, 0.8, line_image, 0.5, 1)

        cv.namedWindow('Video', cv.WINDOW_NORMAL)
        cv.imshow('Video', combo)
    except:
        pass

    if cv.waitKey(2) & 0xFF == ord('q'):
        video.release()
        cv.destroyAllWindows()

video.release()
cv.destroyAllWindows()
