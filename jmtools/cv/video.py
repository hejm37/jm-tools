import numpy as np
from tqdm import tqdm
from PIL import Image
import cv2

import mmcv
from .image import paste_img_at

from jmtools.utils.utils import read_img_dir, join


def get_video_writer(vid_path, shape, fps=25, fourcc='XVID'):
    height, width = shape[0], shape[1]
    resulotion = width, height
    return cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*fourcc), fps,
                           resulotion)


def composite_clips(vid_paths,
                    target_path,
                    layout,
                    blank_size=2,
                    unit_resolution=None,
                    fps=25,
                    fourcc='XVID'):
    vids = []
    row, col = layout
    for i in range(row):
        for j in range(col):
            vid_id = i * col + j
            if vid_id >= len(vid_paths):
                break

            vid = mmcv.VideoReader(vid_paths[vid_id])
            vids.append(vid)

    # Get resolution of composited videos
    source_shape = vids[0][0].shape
    if unit_resolution is not None:
        unit_h, unit_w = unit_resolution
    else:
        unit_h, unit_w = source_shape[0], source_shape[1]
    target_h = unit_h * row + blank_size * (row - 1)
    target_w = unit_w * col + blank_size * (col - 1)
    target_shape = [target_h, target_w]

    # Get size of other channels
    for i in range(2, len(source_shape)):
        target_shape.append(source_shape[i])

    print('Compositing clips to', target_path)
    vwriter = get_video_writer(target_path, target_shape, fps, fourcc)
    for frame_id in tqdm(range(len(vids[0]))):
        composited_img = np.zeros(tuple(target_shape), vids[0][0].dtype)
        for i in range(row):
            for j in range(col):
                vid_id = i * col + j
                if vid_id >= len(vid_paths):
                    break
                img = vids[vid_id][frame_id]
                # resize img if necessary
                img = cv2.resize(img, (1080, 1920))
                img = cv2.resize(img, (unit_w, unit_h))

                paste_img_at(composited_img, img, i, j, blank_size)
        vwriter.write(composited_img)
    vwriter.release()


def seg_to_matte_dir(source_dir, target_dir, single_object=False, auto=True):
    img_ids = read_img_dir(source_dir)

    for img_id in img_ids:
        seg_path = join(source_dir, img_id)
        matte_path = join(target_dir, img_id)

        seg = np.asarray(Image.open(seg_path))
        matte = np.zeros_like(seg)
        if single_object:
            matte[seg == 1] = 255
        else:
            if auto:
                # in auto mode, treat other labels as unknown,
                # let matting model decide if they are fg
                matte[seg == 1] = 255
                matte[seg >= 2] = 128
            else:
                matte[seg >= 1] = 255
        mmcv.imwrite(matte, matte_path)
