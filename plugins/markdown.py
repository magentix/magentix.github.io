"""
Copyright (c) 2022, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
StaPy Markdown Plugin - Version 1.0.0

Requirements:
- markdown
- pymdown-extensions
"""
import markdown
import os
import re


def file_content_opened(content: str, args: dict) -> str:
    if _get_file_extension(args['path']) != 'md':
        return content
    extensions = ['fenced_code', 'tables', 'attr_list', 'md_in_html', 'pymdownx.tilde', 'nl2br']
    content = markdown.markdown(content, tab_length=2, extensions=extensions)
    content = _preformatted_special_chars(content)
    content = _useless_line_break(content)
    return content


def _useless_line_break(content: str) -> str:
    content = content.replace('<br /></li>', '</li>')
    content = content.replace('<br /></p>', '</p>')
    return content


def _preformatted_special_chars(content: str) -> str:
    preformatted = re.findall(r'<pre>(.*?)</pre>', content, flags=re.IGNORECASE | re.DOTALL)
    for pre in preformatted:
        protected = pre.replace('{{', '&lbrace;&lbrace;')
        protected = protected.replace('}}', '&rbrace;&rbrace;')
        protected = protected.replace('{%', '&lbrace;%')
        protected = protected.replace('%}', '%&rbrace;')
        content = content.replace(pre, protected)
    return content


def _get_file_extension(file: str) -> str:
    name, extension = os.path.splitext(file)
    if not extension:
        extension = ''
    return extension.replace('.', '')
