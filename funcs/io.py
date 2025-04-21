import json
import os
import re

from structs.res import AppRes


def read_json(jsonfile: str) -> dict:
    """
    指定された JSON ファイルを読み込む
    :param jsonfile:
    :return:
    """
    with open(jsonfile) as f:
        dict_contents = json.load(f)
    return dict_contents


def get_doe_json(res: AppRes) -> list:
    pattern = re.compile(r'^doe_.+\.json$')
    list_json = list()
    files = sorted(os.listdir(res.dir_config))
    for file in files:
        m = pattern.match(file)
        if m:
            list_json.append(file)
    return list_json
