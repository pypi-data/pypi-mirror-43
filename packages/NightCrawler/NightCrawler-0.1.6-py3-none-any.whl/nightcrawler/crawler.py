#!/bin/env python
# -*- coding: utf-8 -*-

# Author: Grzegorz Szczudlik
# Date: 02.03.19 18:21

import argparse
import sys

if sys.version_info < (3, ):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


from validators import domain, url

from nightcrawler import logger
from nightcrawler.request import PageCrawler
from nightcrawler.sitemap import SitemapGenerator


def target_validator(target):
    if domain(target):
        # http:// should be starting point as secure pages will in fact redirect to https:// eventually
        return urlparse("http://%s/" % target)
    elif url(target):
        # Take into account only valid web protocols
        if target.startswith(("http://", "https://")):
            return urlparse(target)

    raise argparse.ArgumentTypeError("Invalid URL or domain provided: %s" % target)


def main():
    parser = argparse.ArgumentParser(description="Crawler that recursively search for links on sites")
    parser.add_argument("--output", "-o", default=sys.stdout,
                        help="Path to the file to store the output (default: STDOUT)")
    parser.add_argument("--include-external", "-e", dest='include_external', action='store_true', default=False,
                        help="Include external links in the output")
    parser.add_argument("--debug", "-d", dest="level", action='store_const', default=logger.WARN, const=logger.DEBUG,
                        help="Be more verbose over what the script is doing")
    parser.add_argument("URL", metavar="URL|DOMAIN", nargs=1, type=target_validator, help="URL to start crawling from")

    args = parser.parse_args(sys.argv[1:])
    log = logger.getLogger('')
    log.setLevel(args.level)

    pc = PageCrawler(args.URL[0], args.include_external)
    mapping = pc.process()

    sg = SitemapGenerator()
    if isinstance(args.output, str):
        with open(args.output, 'w') as fd:
            sg.generate(mapping, fd)
    else:
        sg.generate(mapping, args.output)
