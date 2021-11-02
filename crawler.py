"""
Copyright (c) 2021, Magentix
This code is licensed under simplified BSD license (see LICENSE for details)
Version 1.6.0
"""
from urllib import request
import json
import time


class StapyCrawler:
    @staticmethod
    def host():
        return 'http://localhost:1985'

    def req(self, method, page=''):
        return request.urlopen(request.Request(self.host() + page, method=method))

    def run(self):
        start = time.clock()
        print('PUT ' + str(self.req('PUT').getcode()))

        pages = json.loads(self.req('GET', '/_pages').read())
        for (page, data) in pages.items():
            if 'enabled' not in data or data['enabled'] == '1':
                print('GET ' + str(self.req('HEAD', page).getcode()) + ' ' + page)

        print('Crawled in ' + str(time.clock() - start) + ' seconds')


def main():
    crawler = StapyCrawler()
    crawler.run()


if __name__ == "__main__":
    main()
