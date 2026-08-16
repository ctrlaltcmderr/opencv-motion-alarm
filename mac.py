import threading
import subprocess
import cv2
import imutils

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not found")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
if start_frame is None:
    print("Error: Could not read from camera")
    cap.release()
    exit()

# FIX 1: Capture baseline in grayscale to match the in-loop format
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0
alarm_lock = threading.Lock()

def beep_alarm():
    global alarm
    for _ in range(5):
        # FIX 3: Read alarm_mode under a lock to avoid race condition
        with alarm_lock:
            if not alarm_mode:
                break
        print("ALARM")
        proc = subprocess.Popen(["afplay", "/System/Library/Sounds/Sosumi.aiff"])
        proc.wait()
    with alarm_lock:
        alarm = False

while True:
    _, frame = cap.read()
    if frame is None:
        continue

    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        # FIX 2: Don't overwrite start_frame — keep the original baseline
        # start_frame = frame_bw  <-- removed

        if threshold.sum() > 300:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        with alarm_lock:
            if not alarm:
                alarm = True
                threading.Thread(target=beep_alarm, daemon=True).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0

        # Refresh baseline snapshot when toggling alarm ON
        if alarm_mode:
            _, snap = cap.read()
            if snap is not None:
                snap = imutils.resize(snap, width=500)
                snap = cv2.cvtColor(snap, cv2.COLOR_BGR2GRAY)
                start_frame = cv2.GaussianBlur(snap, (21, 21), 0)

    if key_pressed == ord("q"):
        with alarm_lock:
            alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()