import os
import json
from data_worker.utils import ROOT_DIR


def _get_wrappers():
    wrapper_files = [
        filename.replace('.py', '')
        for filename in os.listdir(ROOT_DIR + 'wrappers')
        if filename.endswith('_wrapper.py')
    ]

    wrapper_classes = [
        wrapper_file.replace('_', ' ').strip().title().replace(' ', '')
        for wrapper_file in wrapper_files
    ]

    wrapper_names = [
        wrapper_file.replace('_', ' ').replace('wrapper', '').strip().title()
        for wrapper_file in wrapper_files
    ]

    import_string = 'from data_worker.wrappers.{} import {}'

    for wrapper_file, wrapper_class in zip(wrapper_files, wrapper_classes):
        exec(import_string.format(wrapper_file, wrapper_class), globals())

    wrapper_classes = [
        eval(wrapper_class)
        for wrapper_class in wrapper_classes
    ]

    return zip(wrapper_names, wrapper_classes)


def _get_wrapper_alt_names(name):
    names = [name, name.upper(), name.lower()]

    if ' ' in name:
        no_spaces = [x.replace(' ', '') for x in names]
        underscores = [x.replace(' ', '_') for x in names]
        names += no_spaces + underscores

    letters = ''.join(x[0] for x in name.split(' '))
    letters = [letters, letters.lower()]

    names += letters

    return names


def create_api_meta_data(names):
    with open(ROOT_DIR + 'data/api_meta_data.json', 'r') as json_file:
        first_char = json_file.read(1)
        if not first_char:
            meta_data = {}
        else:
            json_file.seek(0)
            meta_data = json.load(json_file)
        for name in names:
            if name in meta_data:
                continue
            meta_data[name] = {}

    with open(ROOT_DIR + 'data/api_meta_data.json', 'w') as json_file:
        json.dump(meta_data, json_file)

    return meta_data


def _check_for_duplicate_alt_names(wrappers):
    names = list(wrappers.keys())
    for i, name1 in enumerate(names):
        for j, name2 in enumerate(names):
            if i == j:
                continue
            duplicates = set(wrappers[name1]['alt_names']).intersection(
                set(wrappers[name2]['alt_names']))
            assert len(duplicates) == 0, "Duplicate alternative names between \'{}\' and \'{}\'.".format(
                name1, name2)


wrappers = {
    wrapper_name: {'class': wrapper_class, 'alt_names': _get_wrapper_alt_names(wrapper_name)}
    for wrapper_name, wrapper_class in _get_wrappers()
}

api_meta_data = create_api_meta_data(list(wrappers.keys()))

_check_for_duplicate_alt_names(wrappers)
