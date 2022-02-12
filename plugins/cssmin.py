"""
Copyright (c) 2022, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
StaPy CssMin Plugin - Version 1.0.0

Requirements:
- rcssmin
"""
from pathlib import Path
import os
import rcssmin


def file_content_opened(content, args: dict) -> str:
    if _get_file_extension(args['path']) != 'css':
        return content
    return rcssmin.cssmin(content)


def file_copy_before(source: str, args: dict) -> str:
    if _get_file_extension(source) != 'css':
        return source
    return _get_min_file(source, rcssmin.cssmin(_get_file_content(source)))


def _get_min_file(source: str, content: str) -> str:
    file = open(_get_tmp_file_path(source), 'w', encoding='utf-8')
    file.write(content)
    file.close()
    return _get_tmp_file_path(source)


def _get_tmp_file_path(source: str) -> str:
    name = os.path.normpath(_get_current_directory() + '/../tmp/' + os.path.basename(source) + '.min')
    _create_directory(name)
    return name


def _create_directory(path) -> None:
    if _get_file_extension(path):
        path = os.path.dirname(path)
    Path(os.path.normpath(path)).mkdir(parents=True, exist_ok=True)


def _get_current_directory() -> str:
    return os.path.dirname(os.path.realpath(__file__))


def _get_file_content(source: str) -> str:
    file = open(os.path.normpath(source), 'r', encoding='utf-8')
    content = str(file.read())
    file.close()
    return content


def _get_file_extension(file: str) -> str:
    name, extension = os.path.splitext(file)
    if not extension:
        extension = ''
    return extension.replace('.', '')
