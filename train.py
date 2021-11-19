#!/usr/bin/env python
import itertools
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.svm import SVC

def main():
    # read in and process landmark data
    data = pd.read_csv('data/landmarked.csv')
    data.set_index(['label', 'index'], inplace=True)
    data = clone_with_variations(data)

    # convert into numpy arrays and integer labels
    y_labels = ['unclassified', '1', '2', '3', 'thumbsup', 'thumbsdown']

    X_data = data.values
    y_data = data.index.get_level_values('label').values
    y_data = np.array([y_labels.index(y) for y in y_data])
    indices = np.arange(len(y_data))
    np.random.shuffle(indices)
    X_data = X_data[indices]
    y_data = y_data[indices]

    # prepare training data
    X_train = X_data[:2000]
    y_train = y_data[:2000]

    # prepare testing data
    X_test = X_data[2000:]
    y_test = y_data[2000:]

    # train SVC
    svc = SVC(C=10**3, gamma=10**-1, kernel='rbf')
    svc.fit(X_train, y_train)
    print(f'Training score: {svc.score(X_train, y_train):.3f}')
    print(f'Testing score: {svc.score(X_test, y_test):.3f}')

    # save model
    with open('model.pkl', 'wb') as file:
        pickle.dump(svc, file, protocol=4)

def draw_landmarks(df_input, rotate_y=0, mirror=False):
    """Draw the landmarks with matplotlib.

    Parameters
    ----------
    df_input : pandas.DataFrame
        The dataframe with the landmarks.
    rotate_y : float, default 0
        The rotation around the y-axis in degrees.
    mirror : bool, default False
        Whether to mirror the landmarks.
    """
    df = df_input.copy()
    if not np.allclose(df.iloc[0], [0, 0, 0]):
        df = pd.DataFrame(np.concatenate(([[0, 0, 0]], df.values)), columns=df.columns)

    if mirror:
        df['x'] = -df['x']

    rotate_y = np.radians(rotate_y)
    df['x'], df['z'] = (
        np.cos(rotate_y) * df['x'] - np.sin(rotate_y) * df['z'],
        np.sin(rotate_y) * df['x'] + np.cos(rotate_y) * df['z']
    )

    z_min, z_max = df.z.min(), df.z.max()
    z_norm = (df.z - z_min) / (z_max - z_min)
    plt.figure(figsize=(6, 6), facecolor='black')
    plt.axis('off')
    plt.gca().set_aspect('equal')
    color = 'white'
    subdf = df.iloc[0:5]; plt.plot(subdf.x, subdf.y, color=color) # thumb
    subdf = df.iloc[5:9]; plt.plot(subdf.x, subdf.y, color=color) # index
    subdf = df.iloc[9:13]; plt.plot(subdf.x, subdf.y, color=color) # middle
    subdf = df.iloc[13:17]; plt.plot(subdf.x, subdf.y, color=color) # ring
    subdf = df.iloc[17:21]; plt.plot(subdf.x, subdf.y, color=color) # pinky
    subdf = df.iloc[[0, 5, 9, 13, 17, 0]]; plt.plot(subdf.x, subdf.y, color=color) # palm
    plt.scatter(
        df.x, df.y,
        color=plt.cm.Reds(1 - z_norm),
        s=180 * z_norm + 20,
        zorder=100,
    )
    plt.show()

def clone_with_variations(data):
    """Artificially increase the number of samples by duplicating the data with
    random noise, mirroring and rotations.
    """
    new_data = []
    for i, row in enumerate(data.iterrows()):
        label, index = row[0]
        df_row = np.reshape(row[1].values, (-1, 3))
        df_row = pd.DataFrame(df_row, columns=['x', 'y', 'z'])

        for i_var, (x_sign, rot_y) in enumerate(itertools.product([+1, -1], [-20, -10, 0, 10, 20])):
            df_ = df_row.copy()
            df_['x'] *= x_sign
            df_['x'], df_['z'] = (
                np.cos(np.radians(rot_y)) * df_['x'] - np.sin(np.radians(rot_y)) * df_['z'],
                np.sin(np.radians(rot_y)) * df_['x'] + np.cos(np.radians(rot_y)) * df_['z']
            )

            # add small noise
            df_ += np.random.normal(0, 0.01, df_.shape)
            flattened_values = np.round(df_.to_numpy().flatten(), 5)
            new_data.append([label, index, i_var, *flattened_values])

    result = pd.DataFrame(
        new_data,
        columns=[
            'label', 'index', 'variation',
            *np.ravel([[f'x{i:02d}', f'y{i:02d}', f'z{i:02d}'] for i in range(1, 21)])
        ],
    )
    result.set_index(['label', 'index', 'variation'], inplace=True)
    return result

if __name__ == '__main__':
    main()