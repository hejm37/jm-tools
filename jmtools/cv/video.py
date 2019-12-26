import numpy as np
from tqdm import tqdm
import cv2

import mmcv
from .image import paste_img_at


def get_video_writer(vid_path,
                     shape,
                     fps=25,
                     fourcc='XVID'):
    height, width = shape[0], shape[1]
    resulotion = width, height
    return cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*fourcc),
                           fps, resulotion)


def composite_clips(vid_paths,
                    target_path,
                    layout,
                    blank_size=2,
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
    source_h, source_w = source_shape[0], source_shape[1]
    target_h = source_h * row + blank_size * (row-1)
    target_w = source_w * col + blank_size * (col-1)
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
                paste_img_at(composited_img, img, i, j, blank_size)
        vwriter.write(composited_img)
    vwriter.release()
