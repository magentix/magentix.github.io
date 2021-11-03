"""
Copyright (c) 2021, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
Magentix Sitemap - Version 1.0.0
"""
from urllib import request
import json


class MagentixSitemap:
    @staticmethod
    def host():
        return 'http://localhost:1985'

    def req(self, method, page='', data=None):
        return request.urlopen(request.Request(self.host() + page, method=method, data=data))

    def run(self):
        pages = json.loads(self.req('GET', '/_pages').read())
        environments = json.loads(self.req('GET', '/_environments').read())
        for env in environments.keys():
            if env == 'local':
                continue
            content = '<?xml version="1.0" encoding="UTF-8"?>' + "\n"
            content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "\n"
            post = False
            for (page, data) in pages.items():
                if 'tags' not in data:
                    continue
                if 'url.' + env not in data:
                    continue
                if 'sitemap' not in data['tags']:
                    continue
                url = data['url.' + env] + page.lstrip('/').replace('index.html', '')
                content += '<url><loc>' + url + '</loc></url>' + "\n"
                post = True
            content += '</urlset>'

            if post:
                data = {'path': 'sitemap.xml', 'content': content, 'env': env}
                self.req('POST', '', str(json.dumps(data)).encode())


def main():
    crawler = MagentixSitemap()
    crawler.run()


if __name__ == "__main__":
    main()
