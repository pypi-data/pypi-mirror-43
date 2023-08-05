#!/bin/env python
# -*- coding: utf-8 -*-

# Author: Grzegorz Szczudlik
# Date: 02.03.19 19:03


class Page(object):
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    def __str__(self):
        return self._url

    def __hash__(self):
        return hash(self._url)

    def __eq__(self, other):
        return self._url.server_url == other.server_url
