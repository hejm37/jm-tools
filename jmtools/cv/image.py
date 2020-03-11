import os
import cv2
import mmcv

from ..utils.utils import get_last_segment, read_img_dir


def wait_key(wait_time=0):
    return cv2.waitKey(wait_time) & 0xFF


def wait_until(key):
    while wait_key() != ord(key):
        pass


def wait_until_q():
    wait_until('q')


def get_rescale(shape, screen_reso=(1080, 1920)):
    rescale = 1
    if shape[0] > screen_reso[0] or shape[1] > screen_reso[1]:
        rescale = min(screen_reso[0]/float(shape[0]),
                      screen_reso[1]/float(shape[1]))
        rescale *= 0.9
    return rescale


def get_ori_coordinate(coor_resized, origin_shape, screen_reso=(1080, 1920)):
    '''Return the coordinate in origin resolution'''
    rescale = get_rescale(origin_shape, screen_reso)
    x_resized, y_resized = coor_resized
    x = x_resized / rescale
    y = y_resized / rescale

    return int(x), int(y)


def resize_img(img, screen_reso=(1080, 1920)):
    shape = img.shape[:2]
    rescale = get_rescale(shape)

    return cv2.resize(img, None, fx=rescale, fy=rescale)


def read_resized_img(img_or_path, screen_reso=(1080, 1920)):
    img = mmcv.imread(img_or_path)

    return resize_img(img, screen_reso)


def display_img(img_or_path,
                winname=None,
                position=(40, 30),
                screen_reso=(1080, 1920)):
    img = read_resized_img(img_or_path, screen_reso)

    if mmcv.is_str(img_or_path) and winname is None:
        img_id = get_last_segment(img_or_path)
        winname = img_id[:-4]
    cv2.namedWindow(winname)
    cv2.moveWindow(winname, position[0], position[1])
    cv2.imshow(winname, img)
    wait_until_q()
    cv2.destroyWindow(winname)


def display_vid(vid_dir, position=(40, 30), screen_reso=(1080, 1920)):
    img_ids = read_img_dir(vid_dir)
    vid_name = get_last_segment(vid_dir)
    cv2.namedWindow(vid_name)
    cv2.moveWindow(vid_name, position[0], position[1])

    for img_id in img_ids:
        img_path = os.path.join(vid_dir, img_id)
        img = read_resized_img(img_path, screen_reso)
        cv2.imshow(vid_name, img)
        if wait_key(1) == ord('q'):
            break
    cv2.destroyWindow(vid_name)


def paste_img_at(composited_img, img, row_idx, col_idx, blank_size):
    '''Paste image to a larger image'''

    # Get paste position
    composited_h, composited_w, = composited_img.shape[0:2]
    source_h, source_w = img.shape[0:2]
    paste_h_start = row_idx * (source_h + blank_size)
    paste_w_start = col_idx * (source_w + blank_size)
    paste_h_end = paste_h_start + source_h
    paste_w_end = paste_w_start + source_w

    composited_img[paste_h_start:paste_h_end, paste_w_start:paste_w_end] = img


def get_palette(num_cls):
    """ Returns the color map for visualizing the segmentation mask.
    Args:
        num_cls: Number of classes
    Returns:
        The color map
    """
    n = num_cls
    palette = [0] * (n * 3)
    for j in range(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i += 1
            lab >>= 3
    return palette
