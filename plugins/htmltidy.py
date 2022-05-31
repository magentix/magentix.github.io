"""
Copyright (c) 2022, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
StaPy HtmlTidy Plugin - Version 1.0.0

Requirements:
- pytidylib
"""
from tidylib import tidy_document
import os


def after_content_parsed(content, args: dict) -> str:
    if _get_page_extension(args['path']) != 'html':
        return content
    document, errors = tidy_document(content, options={'indent': False, 'output-xhtml': True, 'wrap': 0})
    return document


def _get_page_extension(file: str) -> str:
    name, extension = os.path.splitext(file)
    if not extension:
        extension = ''
    return extension.replace('.', '')
