"""
Copyright (c) 2022, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
StaPy HtmlTidy Plugin - Version 1.1.0
"""
import re


def after_content_parsed(content, args: dict) -> str:
    if ((args['file_system']).get_file_extension(args['path'])) != 'html':
        return content
    cleaned = ''
    is_preformatted = False
    for line in content.split('\n'):
        if not is_preformatted and (re.search(r'<pre(.*)>', line, flags=re.IGNORECASE) or re.search(r'<!--', line)):
            is_preformatted = True
        if re.search(r'</pre>', line, flags=re.IGNORECASE) or re.search(r'-->', line):
            is_preformatted = False
        if not is_preformatted and not line.strip():
            continue
        cleaned += (line if is_preformatted else line.strip()) + '\n'
    return cleaned
