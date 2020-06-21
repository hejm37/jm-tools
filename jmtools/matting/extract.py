import numpy as np
import cv2
import os

from jmtools.utils.utils import read_img_dir


def get_img_thrshld(img, matte, threshold=0.5, soft=True, hard=False):
    # return the image extracted by the matte
    if np.max(matte) > 1:
        matte = matte / 255
    mask = matte >= threshold

    filtered = np.zeros_like(img)
    filtered[mask] = img[mask]

    if hard:
        matte[matte > 0.3] = 1

    if soft:
        filtered = filtered * matte[..., None]

    return filtered


def extract_img_thrshld(img_path, matte_path, target=None,
                        threshold=0.8, soft=True, hard=False):
    # return the image and save the image if target is specified
    matte = cv2.imread(matte_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(img_path)

    filtered = get_img_thrshld(img, matte, threshold, soft, hard)

    if target is not None:
        cv2.imwrite(target, filtered)

    return filtered


def extract_img_thrshld_dir(img_dir, matte_dir, target_dir,
                            threshold=0.8, soft=True, hard=False):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    img_ids = read_img_dir(img_dir)

    for img_id in img_ids:
        print('Processing ', img_id)
        img_path = os.path.join(img_dir, img_id)
        matte_path = os.path.join(matte_dir, img_id)
        target = os.path.join(target_dir, img_id)
        extract_img_thrshld(img_path, matte_path, target,
                            threshold, soft, hard)
