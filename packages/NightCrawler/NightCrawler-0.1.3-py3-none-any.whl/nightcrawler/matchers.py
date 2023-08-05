#!/bin/env python
# -*- coding: utf-8 -*-

# Author: Grzegorz Szczudlik
# Date: 02.03.19 20:57

import sys

if sys.version_info < (3, ):
    from urlparse import urlparse, ParseResult
else:
    from urllib.parse import urlparse, ParseResult

from bs4 import BeautifulSoup

from nightcrawler import logger
from nightcrawler.utils import UniqueElasticList, InvalidURL


class AnchorMatcher(object):
    def __init__(self, list_class=UniqueElasticList):
        self.__list_cls = list_class

    def parse(self, content, url):
        results = self.__list_cls()

        log = logger.getLogger('matchers.AnchorMatcher')
        log.debug("Parsing content")

        parser = BeautifulSoup(content, "lxml")
        for item in parser.find_all("a"):
            if item is None:
                continue

            try:
                href = urlparse(item.get("href", ""))
            except InvalidURL:
                continue

            if href.scheme not in ('', 'http', 'https') or (href.netloc and href.netloc != url.netloc):
                continue

            href = ParseResult(
                scheme=href.scheme if href.scheme else url.scheme,
                netloc=href.netloc if href.netloc else url.netloc,
                path=href.path if href.path else "/",
                params=href.params,
                query=href.query,
                fragment=''
            )

            results.append(href)
            log.debug('Found url: {url}'.format(url=href.geturl()))

        return results
