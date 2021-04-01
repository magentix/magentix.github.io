"""
Copyright (c) 2021, Magentix
This code is licensed under simplified BSD license license (see LICENSE for details)
Version 1.3.0
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
import shutil
import os
import json


class StapyFileSystem:
    @staticmethod
    def get_content_types():
        return {
            'html': 'text/html; charset=utf-8',
            'xml': 'text/xml; charset=utf-8',
            'css': 'text/css; charset=utf-8',
            'js': 'application/javascript; charset=utf-8',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'gif': 'image/gif',
            'ico': 'image/x-icon'
        }

    @staticmethod
    def get_root_dir():
        return os.path.dirname(os.path.abspath(__file__)) + os.sep

    def get_web_dir(self):
        return self.get_root_dir() + 'web'

    def get_build_dir(self, directory=''):
        return self.get_root_dir() + 'build' + (os.sep + directory if directory else '')

    @staticmethod
    def get_file_content(path, mode='r'):
        encoding = 'utf-8' if mode == 'r' else None
        file = open(os.path.normpath(path), mode, encoding=encoding)
        content = file.read()
        file.close()

        return content

    @staticmethod
    def get_file_extension(file):
        name, extension = os.path.splitext(file)
        if not extension:
            extension = ''

        return extension.replace('.', '')

    def get_content_type(self, extension):
        types = self.get_content_types()
        if extension in types:
            return types[extension]

        return 'text/plain; charset=utf-8'

    def get_file_type(self, file):
        return self.get_content_type(self.get_file_extension(file))

    def create_directory(self, path):
        if self.get_file_extension(path):
            path = os.path.dirname(path)

        Path(os.path.normpath(path)).mkdir(parents=True, exist_ok=True)

    def create_file(self, path, content=''):
        path = os.path.normpath(path)
        self.create_directory(path)
        file = open(path, "w")
        file.write(content)
        file.close()

    def copy_tree(self, src, dst):
        src = os.path.normpath(src)
        dst = os.path.normpath(dst)
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                self.copy_tree(s, d)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    shutil.copy2(s, d)

    @staticmethod
    def merge_json(*files):
        merged = json.loads('{}')
        for file in files:
            f = open(file, encoding='utf-8')
            data = json.load(f)
            f.close()
            for (key, value) in data.items():
                merged[key] = value

        return merged


class StapyParser:
    fs = StapyFileSystem()

    def process(self, data, content):
        content = self.template_tags(data, content)
        content = self.content_tags(data, content)

        return content

    @staticmethod
    def content_tags(data, content):
        for (key, value) in data.items():
            content = content.replace('{{ ' + key + ' }}', value if value else '')

        return content

    def template_tags(self, data, content, parent=''):
        for (key, value) in data.items():
            if key != parent and '{% ' + key + ' %}' in content:
                base = self.fs.get_root_dir()
                content = content.replace(
                    '{% ' + key + ' %}',
                    self.template_tags(data, self.fs.get_file_content(base + value), key) if value else ''
                )

        return content


class StapyHTTPRequestHandler(BaseHTTPRequestHandler):
    fs = StapyFileSystem()
    ps = StapyParser()

    def do_GET(self):
        result = self.copy_resources()

        if result is None:
            try:
                result = self.get_html()
            except OSError:
                try:
                    result = self.get_file()
                except OSError:
                    result = self.get_error()

        self.send_response(result['status'])
        self.send_header('Content-type', result['type'])
        self.end_headers()
        self.wfile.write(result['content'])

    def send_response(self, code, message=None):
        self.send_response_only(code, message)
        self.send_header('Date', self.date_time_string())

    def copy_resources(self):
        try:
            self.fs.copy_tree(self.fs.get_build_dir('web'), self.fs.get_web_dir())
        except Exception as e:
            return self.get_response(500, self.fs.get_content_type('html'), str(e).encode())

    def get_error(self):
        return self.get_response(404, self.fs.get_content_type('html'), b'404 not found')

    def get_file(self):
        content = self.fs.get_file_content(self.fs.get_web_dir() + self.path, 'rb')

        return self.get_response(200, self.fs.get_file_type(self.path), content)

    def get_html(self):
        status = 500
        data = self.fs.merge_json(self.get_default_config(), self.get_page_config())
        try:
            content = self.fs.get_file_content(self.fs.get_root_dir() + data['template'])
            content = self.ps.process(data, content)
            self.save_html(content)
            status = 200
        except Exception as e:
            content = str(e)

        return self.get_response(status, self.fs.get_content_type('html'), content.encode())

    def save_html(self, content):
        self.fs.create_file(self.fs.get_web_dir() + self.get_page_path(), content)

    def get_page_path(self):
        path = self.path
        if not path.endswith('/') and '.' not in path:
            path += '/'

        if path.endswith('/'):
            path = path + 'index.html'

        return path

    def get_page_config(self):
        return os.path.normpath(self.fs.get_build_dir('json') + self.get_page_path() + '.json')

    def get_default_config(self):
        return os.path.normpath(self.fs.get_build_dir('json') + os.sep + 'default.json')

    @staticmethod
    def get_response(status, file_type, content):
        return {'status': status, 'type': file_type, 'content': content}


class StapyHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    try:
        httpd = StapyHTTPServer(('localhost', 1985), StapyHTTPRequestHandler)
        print('Serving under http://' + httpd.server_name + ':' + str(httpd.server_port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nGood bye!")


if __name__ == "__main__":
    main()
