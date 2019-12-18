import os
import cv2

from ..utils.utils import get_last_segment, read_img_dir


def get_rescale(shape, screen_reso=(1080, 1920)):
    rescale = 1
    if shape[0] > screen_reso[0] or shape[1] > screen_reso[1]:
        rescale = min(screen_reso[0]/float(shape[0]),
                      screen_reso[1]/float(shape[1]))
        rescale *= 0.9
    return rescale


def wait_until(key):
    while cv2.waitKey(0) & 0xFF != ord(key):
        pass


def wait_until_q():
    wait_until('q')


def read_resized_img(img_path, screen_reso=(1080, 1920)):
    img = cv2.imread(img_path)
    shape = img.shape[:2]
    rescale = get_rescale(shape)

    return cv2.resize(img, None, fx=rescale, fy=rescale)


def display_img(img_path, position=(40, 30), screen_reso=(1080, 1920)):
    img = read_resized_img(img_path, screen_reso)

    img_id = get_last_segment(img_path)
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow(vid_name)
