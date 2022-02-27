from glob import glob
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

import cv2

def get_gesture_labels(directory='./raw/'):
    """Returns a list of gesture labels.

    Gesture labels are given by the subdirectories of the given directory, e.g.
    "./raw/thumbsup" gives "thumbsup" label.

    Parameters
    ----------
    directory : str, default './raw/'
        Directory containing folders of images.
    
    Returns
    -------
    labels : list of str
        List of gesture labels, e.g. ``['1', '2, '3', 'thumbsup', 'thumbsdown']``.
    """
    labels = []
    paths = glob(str(Path(directory) / '*'))
    for path in paths:
        path = Path(path)
        if path.is_dir():
            labels.append(path.stem)
    return labels

def rename_images(directory='./raw/', label=None):
    '''Rename images into enumerated names, e.g. "img-0001.jpg".

    Parameters
    ----------
    directory : str, default './raw/'
        Directory containing folders of images.
    label : str, default None
        If not None, only rename images of this label. Otherwise, rename all
        images under all labels.
    '''
    if label is None:
        labels = get_gesture_labels(directory)
        for label in labels:
            rename_images(directory, label) # recursion
        return

    paths = glob(str(Path(directory) / label / '*'))
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # rename and move all images to tmpdir
        i = 1
        tmppaths = []
        for path in paths:
            path = Path(path)
            if path.is_dir():
                rename_images(path, recursive=False)

            if path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                continue
            tmppaths.append(tmpdir / f'img-{i:04d}{path.suffix}')
            shutil.move(path, tmppaths[-1])
            i += 1
        
        # move all images to directory
        for tmppath in tmppaths:
            path = Path(directory) / label / tmppath.name
            shutil.move(tmppath, path)

def remove_all(glob_pattern):
    """Remove all files matching the glob pattern.

    Parameters
    ----------
    glob_pattern : str
        Glob pattern of files to be removed.
    """
    paths = glob(glob_pattern)
    for path in paths:
        path = Path(path)
        path.unlink()

def pad_image(image, target_size=480):
    """Pad image into square dimension.

    Parameters
    ----------
    image : ndarray
        Image to be padded.
    target_size : int, default 480
        Target size of the padded square image.
    
    Returns
    -------
    padded_image : ndarray
        Padded image.
    """
    if image.shape[0] > image.shape[1]: # y is longer; tall image
        y_pixels = target_size
        x_pixels = int(image.shape[1] * y_pixels / image.shape[0])
        pad_kw = dict(
            top=0, bottom=0, left=0,
            right=target_size - x_pixels,
        )
    else: # x is longer; wide image
        x_pixels = target_size
        y_pixels = int(image.shape[0] * x_pixels / image.shape[1])
        pad_kw = dict(
            left=0, right=0, top=0,
            bottom=target_size - y_pixels,
        )
    image = cv2.resize(image, (x_pixels, y_pixels))
    image = cv2.copyMakeBorder(image, borderType=cv2.BORDER_CONSTANT, **pad_kw)
    return image

def get_landmarks(image, hand_tracker):
    """Get Mediapipe's hand landmarks from image.

    Parameters
    ----------
    image : ndarray
        Image to be analyzed.
    hand_tracker : HandTracker instance
        HandTracker instance.
    
    Returns
    -------
    image : ndarray
        Image with landmarks drawn in-place.
    df_hand : pandas.DataFrame
        DataFrame containing hand landmarks. There are 21 rows. Each row
        corresponds to one single hand landmark coordinate point (x, y, z) that
        has been normalized.  To learn more about how normalization is done,
        see `:py:func:`normalize_hand` in `:py:class:`HandTracker`.
    """
    image = hand_tracker.process_frame(image)
    df_hand = None
    if hand_tracker.found_hand():
        df_hand = hand_tracker.get_all_hand_dataframes(image)[0]
        hand_tracker.draw_all_hands(image)
    return image, df_hand

if __name__ == '__main__':
    # create the hand tracker instance
    import sys
    mod_dir = str(Path(__file__).parent.parent.resolve())
    if mod_dir not in sys.path:
        sys.path.append(mod_dir)
    from recognition import HandTracker
    hand_tracker = HandTracker(max_num_hands=1, static_image_mode=True)

    # process (identify landmarks) all images in the raw directory
    gestures = get_gesture_labels()
    rename_images()
    remove_all('./processed/csv_files/*')
    remove_all('./processed/png_files/*')
    for gesture in gestures:
        print(f'Processing gesture "{gesture}"...')
        paths = glob(str(Path('./raw') / gesture / '*.*'))
        for path in paths:
            path = Path(path)
            print(f'\r\t> "{path.stem}"', end='', flush=True)

            image = cv2.imread(str(path))
            image = pad_image(image)
            image, df_hand = get_landmarks(image, hand_tracker)
            if df_hand is None:
                print(f'No hand found for "{path}"')
                continue

            # save image result
            out_path = Path('./processed/png_files') / f'g{gesture}-{path.stem[4:]}.png'
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(out_path), image)

            # save landmarks result
            out_path = Path('./processed/csv_files') / f'g{gesture}-{path.stem[4:]}.csv'
            df_hand.to_csv(out_path, index=False, header=False)
        print()
    print('Done!')