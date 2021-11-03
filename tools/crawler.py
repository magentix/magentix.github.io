"""
Copyright (c) 2021, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
StaPy Crawler - Version 1.0.0
"""
from urllib import request
import json
import time
import sys


class StapyCrawler:
    @staticmethod
    def host():
        return 'http://localhost:1985'

    def req(self, method, page=''):
        return request.urlopen(request.Request(self.host() + page, method=method))

    def run(self):
        start = time.clock()

        if self.can_delete():
            self.delete()

        if self.can_copy():
            self.copy()

        if self.can_crawl():
            self.crawl()

        print('Time: ' + str(round((time.clock() - start) * 100, 2)) + 'ms')

    def delete(self):
        print('DELETE ' + str(self.req('DELETE').getcode()))

    def copy(self):
        print('PUT ' + str(self.req('PUT').getcode()))

    def crawl(self):
        pages = json.loads(self.req('GET', '/_pages').read())
        for (page, data) in pages.items():
            if 'enabled' not in data or data['enabled'] == '1':
                print('HEAD ' + str(self.req('HEAD', page).getcode()) + ' ' + page)

    @staticmethod
    def can_delete():
        for arg in sys.argv:
            if arg == 'delete' or arg == 'full':
                return True
        return False

    @staticmethod
    def can_copy():
        for arg in sys.argv:
            if arg == 'copy' or arg == 'full':
                return True
        return False

    @staticmethod
    def can_crawl():
        for arg in sys.argv:
            if arg == 'crawl' or arg == 'full':
                return True
        return False


def main():
    crawler = StapyCrawler()
    crawler.run()


if __name__ == "__main__":
    main()
