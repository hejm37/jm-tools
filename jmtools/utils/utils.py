import os
import base64


def read_list(filename):
    print("Reading list from file", filename)
    return open(filename).read().splitlines()


def read_img_dir(img_dir):
    print("Reading from directory", img_dir)
    img_ids = os.listdir(img_dir)
    img_ids = [img_id for img_id in img_ids if img_id[-4:] == '.png']
    img_ids.sort()
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
