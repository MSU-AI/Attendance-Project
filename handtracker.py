#!/usr/bin/env python
import json
import time

import cv2
import mediapipe as mp
import pandas as pd

with open('finger_index.json', 'r') as file:
    content = json.load(file)
    finger_index = {name: id_ for id_, name in enumerate(content['index'])}

def main():
    # initialize camera (webcam) from ID 0 (could be a different ID if multiple webcams)
    cap = cv2.VideoCapture(0)

    # initialize hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    mp_draw = mp.solutions.drawing_utils

    prev_time, current_time = 0, 0

    # main video loop
    while True:
        # get frame from camera
        success, frame = cap.read()

        # process RGB frame
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        gesture = 'unclassified'
        df_pixels = []
        if result.multi_hand_landmarks is not None: # at least one hand detected
            # loop over all the hands
            for hand_landmarks in result.multi_hand_landmarks:
                # convert fractional landmark coordinates into pixel coordinates
                for id_, lm in enumerate(hand_landmarks.landmark):
                    height, width, _ = frame.shape
                    pixel_x, pixel_y = int(lm.x * width), int(lm.y * height)
                    df_pixels.append([id_, pixel_x, pixel_y])

                # draw the hand on the frame
                mp_draw.draw_landmarks(
                    frame, hand_landmarks,
                    connections=mp_hands.HAND_CONNECTIONS,
                )
            df_pixels = pd.DataFrame(df_pixels, columns=['id', 'x', 'y'])
            df_pixels.set_index('id', inplace=True, drop=False)

            # some statistics
            gesture_stats = dict(
                x_mean=df_pixels.x.mean(),
                y_mean=df_pixels.y.mean(),
                x_std=df_pixels.x.std(),
                y_std=df_pixels.y.std(),
            )

            # determine gestures
            if is_gesture_one(df_pixels, gesture_stats):
                gesture = 'one'
        
        # calculate frame rate (fps)
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # display frame and other info
        cv2.putText(
            frame, f'FPS:{fps:3.0f}',
            (10, 20),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=1,
            color=(0, 0, 255),
            thickness=2,
        )
        cv2.putText(
            frame, f'{gesture}',
            (10, 50),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=2,
            color=(0, 255, 0) if gesture != 'unclassified' else (255, 0, 0),
            thickness=2,
        )
        cv2.imshow('img', frame)
        time.sleep(0.04) # optional

        # break if key 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # release camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

def is_gesture_one(df_pixels, gesture_stats):
    global finger_index
    pix = df_pixels
    stats = gesture_stats
    x_thres = 1.5 * stats['x_std']
    y_thres = 1.5 * stats['y_std']

    cond_1 = pix.id.iloc[pix.y.argmin()] == finger_index['index_finger_tip']
    cond_2 = (
        pix.loc[finger_index['thumb_tip'], 'x']  - stats['x_mean'] < x_thres
        and pix.loc[finger_index['middle_finger_tip'], 'x'] - stats['x_mean'] < x_thres
        and pix.loc[finger_index['ring_finger_tip'], 'x'] - stats['x_mean'] < x_thres
        and pix.loc[finger_index['pinky_tip'], 'x'] - stats['x_mean'] < x_thres
    )
    cond_3 = (
        pix.loc[finger_index['index_finger_tip'], 'y'] - stats['y_mean'] < y_thres
        and pix.loc[finger_index['middle_finger_tip'], 'y'] - stats['y_mean'] < y_thres
        and pix.loc[finger_index['ring_finger_tip'], 'y'] - stats['y_mean'] < y_thres
        and pix.loc[finger_index['pinky_tip'], 'y'] - stats['y_mean'] < y_thres
    )
    return cond_1 and cond_2 and cond_3

if __name__ == '__main__':
    main()