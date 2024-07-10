import cv2
import time

cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (frame_width, frame_height))

start_time = time.time()

while True:
    ret, frame = cap.read()
    if ret:
        out.write(frame)

        if time.time() - start_time > 120:
            break
    else:
        break

cap.release()
out.release()
