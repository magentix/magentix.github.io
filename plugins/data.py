"""
Copyright (c) 2022, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
Magentix Data Plugin - Version 1.0.0
"""
from datetime import datetime


def page_data_merged(data: dict, args: dict) -> dict:
    data['year'] = datetime.now().year
    return data
