# OpenCV Motion Alarm

A real-time motion detection system built using **Python** and **OpenCV**. The application monitors a webcam feed, detects motion, and plays an alarm sound whenever significant movement is detected.

## Features

- Real-time motion detection using webcam
- Motion highlighted using frame differencing
- Alarm triggered when continuous motion is detected
- Toggle motion detection on/off during runtime
- Cross-platform support:
  - **macOS** (`afplay`)
  - **Windows** (`winsound`)

## Technologies Used

- Python 3
- OpenCV
- imutils
- threading

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ctrlaltcmderr/opencv-motion-alarm.git
cd opencv-motion-alarm
```

2. Install the required packages:

```bash
pip install opencv-python imutils
```

## Running the Project

### macOS

```bash
python mac.py
```

### Windows

```bash
python motion_detection.py
```

## Controls

| Key | Action |
|-----|--------|
| **T** | Toggle motion detection ON/OFF |
| **Q** | Quit the application |

## How It Works

1. The application captures an initial background frame.
2. Each incoming frame is converted to grayscale and blurred.
3. The current frame is compared with the background frame.
4. If continuous motion is detected, an alarm sound is played.
5. Press **T** to enable or disable motion detection at any time.

## Project Structure

```
opencv-motion-alarm/
├── mac.py
├── motion_detection.py
├── README.md
```

## Future Improvements

- Adjustable motion sensitivity
- Save snapshots or recordings when motion is detected
- Email or desktop notifications

## License

This project is open-source and intended for learning and educational purposes.
