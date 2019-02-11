#!/usr/bin/env python
# -*- coding: UTF-8 -*
import urllib


class urlUtil(object):
    instance = None

    @staticmethod
    def getInstance():
        if urlUtil.instance is None:
            urlUtil.instance = urlUtil()
        return urlUtil.instance

    def getQuoteFromUrl(self, url):
        urlParese = urllib.parse.urlparse(url)
        return urllib.parse.parse_qs(urlParese.query, True)

    def getApitPathFromUrl(self, url):
        urlParese = urllib.parse.urlparse(url)
        return urllib.parse.parse_qs(urlParese.query, True)