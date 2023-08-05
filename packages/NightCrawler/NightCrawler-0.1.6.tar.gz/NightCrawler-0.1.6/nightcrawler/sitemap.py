#!/bin/env python
# -*- coding: utf-8 -*-

# Author: Grzegorz Szczudlik
# Date: 03.03.19 14:38

from bs4 import BeautifulSoup
from nightcrawler import logger


class SitemapGenerator(object):
    log = logger.getLogger('sitemap.SitemapGenerator')
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"

    def generate(self, result_set, fd):
        self.log.debug("Generating sitemap")
        xml = BeautifulSoup(features="lxml-xml")
        urlset = xml.new_tag("urlset", xmlns=self.namespace)

        for result in result_set:
            url = self.__generate_entry(xml, result)
            urlset.append(url)
            xml.append(urlset)

        self.log.debug("Writing map to disk")
        fd.write(xml.prettify())

        self.log.debug("Sitemap generated")

    def __generate_entry(self, soup, item):
        self.log.debug("Generating entry for %s" % item.geturl())
        url = soup.new_tag("url")

        loc = soup.new_tag("loc")
        loc.string = item.geturl()
        url.append(loc)

        return url
