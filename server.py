"""
Copyright (c) 2021, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
Version 1.5.1
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
import json
import os
import mimetypes
import re
import shutil


class StapyFileSystem:
    environments = {}

    @staticmethod
    def get_root_dir():
        return os.path.dirname(os.path.abspath(__file__)) + os.sep

    def get_build_dir(self):
        return self.get_root_dir() + 'web'

    def get_source_dir(self, directory=''):
        return self.get_root_dir() + 'source' + (os.sep + os.path.normpath(directory) if directory else '')

    @staticmethod
    def get_local_environment():
        return 'local'

    def get_environments(self):
        if not self.environments:
            self.environments[self.get_local_environment()] = False
            for env in os.listdir(self.get_build_dir()):
                path = os.path.join(self.get_build_dir(), env)
                if os.path.isdir(path):
                    self.environments[env] = path

        return self.environments

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

    @staticmethod
    def get_file_type(file):
        mime, encoding = mimetypes.guess_type(file)
        if encoding:
            return f"{mime}; charset={encoding}"
        else:
            return mime or "application/octet-stream"

    @staticmethod
    def get_html_file_type():
        return 'text/html; charset=utf-8'

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
            if os.path.exists(file):
                f = open(file, encoding='utf-8')
                data = json.load(f)
                f.close()
                for (key, value) in data.items():
                    merged[key] = value

        return merged


class StapyParser:
    fs = StapyFileSystem()

    def process(self, data, content, env):
        content = self.template_tags(data, content, env)
        content = self.content_tags(data, content, env)

        return content

    def content_tags(self, data, content, env):
        for var, value in sorted(data.items(), reverse=True):
            content = content.replace('{{ ' + self.get_var(var, env) + ' }}', value if value else '')

        return content

    def template_tags(self, data, content, env, parent=''):
        for var, value in sorted(data.items(), reverse=True):
            key = self.get_var(var, env)
            if key != parent and '{% ' + key + ' %}' in content:
                file = self.fs.get_source_dir(value)
                content = content.replace(
                    '{% ' + key + ' %}',
                    self.template_tags(data, self.fs.get_file_content(file), key) if value else ''
                )

        return content

    @staticmethod
    def get_var(var, env):
        return re.sub(r'\.' + env + '$', '', var)


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
        try:
            self.wfile.write(result['content'])
        except BrokenPipeError:
            pass

    def send_response(self, code, message=None):
        self.send_response_only(code, message)
        self.send_header('Date', self.date_time_string())

    def copy_resources(self):
        try:
            for directory in self.fs.get_environments().values():
                if directory:
                    self.fs.copy_tree(self.fs.get_source_dir('web'), directory)
        except Exception as e:
            return self.get_response(500, self.fs.get_html_file_type(), str(e).encode())

    def get_error(self):
        return self.get_response(404, self.fs.get_html_file_type(), b'404 not found')

    def get_file(self):
        file = self.fs.get_source_dir('web') + self.path

        return self.get_response(200, self.fs.get_file_type(file), self.fs.get_file_content(file, 'rb'))

    def get_html(self):
        status = 500
        content = ''
        self.fs.get_file_content(self.get_page_config())
        try:
            data = self.fs.merge_json(self.get_page_config('/default'), self.get_page_config())
            template = self.fs.get_file_content(self.fs.get_source_dir(data['template']))
            for env in self.fs.get_environments().keys():
                result = self.ps.process(data, template, env)
                if env == self.fs.get_local_environment():
                    content = result
                else:
                    self.save_html(result, env)
            status = 200
        except Exception as e:
            content = str(e)

        return self.get_response(status, self.fs.get_html_file_type(), content.encode())

    def save_html(self, content, env):
        self.fs.create_file(self.fs.get_environments()[env] + self.get_page_path(), content)

    def get_page_path(self):
        path = self.path
        if not path.endswith('/') and '.' not in path:
            path += '/'

        if path.endswith('/'):
            path = path + 'index.html'

        return path

    def get_page_config(self, path=None):
        return os.path.normpath(self.fs.get_source_dir('json') + (self.get_page_path() if not path else path) + '.json')

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
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
