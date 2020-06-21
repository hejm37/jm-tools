import os
import base64


def listdir(dir, dir_only=False):
    filelist = os.listdir(dir)
    if dir_only:
        filelist = [
            item for item in filelist if os.path.isdir(join(dir, item))
        ]
    filelist.sort()
    return filelist


def read_list(filepath):
    print("Reading list from file", filepath)
    with open(filepath, 'r') as f:
        return f.read().splitlines()


def write_str_list(str_list, filepath):
    print("Writing string list to file", filepath)
    with open(filepath, 'w') as f:
        for string in str_list:
            f.write(string + '\n')


def read_img_dir(img_dir, img_ext='.png'):
    print("Reading from directory", img_dir)
    img_ids = listdir(img_dir)
    img_ids = [img_id for img_id in img_ids if img_id.endswith(img_ext)]
    return img_ids


def get_last_segment(path):
    return os.path.basename(os.path.normpath(path))


def base64_decode(string_path, save_path):
    with open(string_path, 'rb') as f:
        raw_str = f.read()

    decoded_data = base64.b64decode(raw_str)

    with open(save_path, 'wb') as f:
        f.write(decoded_data)


# Shorter name for join
join = os.path.join
