import re
import mmcv
import torch


def modify_state_dict_(state_dict, pattern_mappings):
    for key in list(state_dict.keys()):
        new_key = None
        for pattern, transfer_pattern in pattern_mappings.items():
            pattern = re.compile(pattern)
            pattern = pattern.match(key)
            if pattern is not None:
                new_key = transfer_pattern(pattern.groups())
                state_dict[new_key] = state_dict[key]
                del state_dict[key]
                continue

        if new_key is None:
            print(f'No matched patter for key {key}')
            del state_dict[key]
        else:
            print(f'{key}, {new_key}')


def modify_state_dict(source_weight_path, save_weight_path, pattern_mappings):
    checkpoint = torch.load(source_weight_path)
    modify_state_dict_(checkpoint['state_dict'], pattern_mappings)
    torch.save(checkpoint, save_weight_path)


def remap_keys_(seq, pattern_mappings):
    new_seq = []
    for string in seq:
        new_string = None
        for pattern, transfer_pattern in pattern_mappings.items():
            pattern = re.compile(pattern)
            pattern = pattern.match(string)
            if pattern is not None:
                new_string = transfer_pattern(pattern.groups())

        if new_string is None:
            new_string = string
            print(f'No matched patter for string {string}')

        new_seq.append(new_string)
    return new_seq


def remap_keys(source_weight_list_path, save_weight_list_path,
               pattern_mappings):
    old_list = mmcv.list_from_file(source_weight_list_path)
    old_list = [item.strip('\'') for item in old_list]
    new_list = mmcv.list_from_file(save_weight_list_path)
    new_list = [item.strip('\'') for item in new_list]

    old_list_mapped = remap_keys_(old_list, pattern_mappings)

    difference = set(old_list_mapped).difference(new_list)
    intersection = set(old_list_mapped).intersection(new_list)

    return difference, intersection
