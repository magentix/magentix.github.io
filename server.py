"""
Copyright (c) 2021, Magentix
This code is licensed under simplified BSD license license (see LICENSE for details)
Version 1.3.0
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
import shutil
import ssl
import argparse
import os
import json
import re


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
        return os.path.dirname(os.path.abspath(__file__)) + '/'

    @staticmethod
    def get_file_content(path, mode='r'):
        file = open(path, mode)
        content = file.read()
        file.close()

        return content

    def get_web_dir(self):
        return self.get_root_dir() + 'web'

    def get_build_dir(self):
        return self.get_root_dir() + 'build'

    def copy_tree(self, src, dst):
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
                file = self.fs.get_root_dir() + value
                content = content.replace(
                    '{% ' + key + ' %}',
                    self.template_tags(data, self.fs.get_file_content(file), key) if value else ''
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
            self.fs.copy_tree(self.fs.get_build_dir() + '/web', self.fs.get_web_dir())
        except Exception as e:
            return {'status': 500, 'type': 'text/html; charset=utf-8', 'content': str(e).encode()}

    @staticmethod
    def get_error():
        return {'status': 404, 'type': 'text/html; charset=utf-8', 'content': b'404 not found'}

    def get_file(self):
        content = self.fs.get_file_content(self.fs.get_web_dir() + self.path, 'rb')

        return {'status': 200, 'type': self.get_content_type(), 'content': content}

    def get_html(self):
        status = 500
        with open(self.get_page_config()) as file:
            try:
                data = json.load(file)
                file.close()
                content = self.fs.get_file_content(self.fs.get_root_dir() + data['template'])
                content = self.ps.process(data, content)
                self.save_html(content)
                status = 200
            except Exception as e:
                content = str(e)

        return {'status': status, 'type': 'text/html; charset=utf-8', 'content': content.encode()}

    def save_html(self, content):
        file = self.fs.get_web_dir() + self.get_page_path()
        Path(os.path.dirname(file)).mkdir(parents=True, exist_ok=True)
        html = open(file, "w")
        html.write(content)
        html.close()

    def get_file_extension(self):
        name, extension = os.path.splitext(self.path)
        if not extension:
            extension = ''

        return extension.replace('.', '')

    def get_content_type(self):
        types = self.fs.get_content_types()

        if self.get_file_extension() in types:
            return types[self.get_file_extension()]

        return 'text/plain; charset=utf-8'

    def get_page_path(self):
        path = self.path
        if not path.endswith('/') and '.' not in path:
            path += '/'

        if path.endswith('/'):
            path = path + 'index.html'

        return path

    def get_page_config(self):
        path = self.get_page_path()

        return self.fs.get_build_dir() + '/json' + path + '.json'


class StapyHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    parser = argparse.ArgumentParser(
        prog="Stapy",
        description="Real-time static site generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    group = parser.add_argument_group("server configuration")
    group.add_argument("--hostname", help="Server hostname", default='localhost')
    group.add_argument("--port", help="Server port to bind to", type=int, default=1985)
    group.add_argument("--tls-certfile", dest="certfile", help="Server TLS certificate file", metavar="FILE")
    group.add_argument("--tls-keyfile", dest="keyfile", help="Server TLS private key file", metavar="FILE")
    args = parser.parse_args()

    httpd = StapyHTTPServer((args.hostname, args.port), StapyHTTPRequestHandler)

    protocol = 'http'
    if args.certfile is not None and args.keyfile is not None:
        httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=args.keyfile, certfile=args.certfile, server_side=True)
        protocol = 'https'

    try:
        print('Serving under ' + protocol + '://' + httpd.server_name + ':' + str(httpd.server_port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nGood bye!")


if __name__ == "__main__":
    main()
