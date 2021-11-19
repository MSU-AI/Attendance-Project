# Interaction branch (Hand gesture recognition)

> Warning: Currently, this branch is only developed as a standalone software running on Ubuntu (most likely would work on other Linux environment; not tested yet).

## How to install?
```bash
python3 -m venv ./venv                      # create virtual environment
source ./venv/bin/activate                  # activate environment
python -m pip install -r requirements.txt   # install dependencies
```

## How to use?
Make sure a camera is connected to the computer, then run the following command:
```bash
python handtracker.py
```
Currently, only five gestures are supported:
- One (index finger up)
- Two (index finger and middle finger up)
- Three (index finger, middle finger and ring finger up)
- Thumbs up
- Thumbs down

## How to train?
This is still under development. For now, we have a very simple model that train on ~300 labeled landmarks; see [`landmarked.csv`](data/landmarked.csv). The trained model is saved as [`model.pkl`](model.pkl). To train the model, run the following command:
```bash
python train.py
```

## What is a landmark?
Landmark, or hand landmark, is a point on the hand that is used to detect the hand. In this project, we use the hand tracking solutions by [MediaPipe](https://google.github.io/mediapipe/solutions/hands) to detect the 21 landmarks. Then we train our own model to classify the hand gesture using the (x, y, z) coordinates of the landmarks. Below is a figure showing the indices of the landmarks, which are stored in [`finger_index.json`](finger_index.json).
![Landmarks](hand-landmarks.png)
