#!/bin/env python
# -*- coding: utf-8 -*-

# Author: Grzegorz Szczudlik
# Date: 02.03.19 22:33

import sys

if sys.version_info < (3, ):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


__all__ = ['ElasticList', 'UniqueElasticList', 'URL', 'InvalidURL']


# This class could implement more magic methods but for given task - it won't unless needed
class ElasticList(object):
    def __init__(self, *args):
        self._queue = []
        self._queue.extend(args)
        self._iter = None

    def __str__(self):
        return str(self._queue)

    def __repr__(self):
        return repr(self._queue)

    def push(self, item):
        self._queue.append(item)
    append = push

    def pop(self):
        if self._iter is not None:
            self._iter -= 1
        return self._queue.pop(0)

    def extend(self, collection):
        self._queue.extend(collection)

    def values(self):
        return self._queue[:]

    def __len__(self):
        return len(self._queue)

    def __contains__(self, item):
        return item in self._queue

    def __iter__(self):
        self._iter = 0
        return self

    def __getitem__(self, index):
        return self._queue[index]

    def __next__(self):
        if self._iter is None or len(self._queue)-1 < self._iter:
            self._iter = None
            raise StopIteration()

        value = self._queue[self._iter]
        self._iter += 1
        return value


class UniqueElasticList(ElasticList):
    def __init__(self, *args):
        super().__init__(*args)

    def push(self, item):
        if item not in self._queue:
            self._queue.append(item)
    append = push

    def extend(self, collection):
        for item in collection:
            self.push(item)


class InsensitiveString(str):
    def __init__(self, value):
        super(str).__init__(value)
        self.__value = value

    def __eq__(self, other):
        return self.__value.lower == other.lower()


# Invalid URL Exception - to distinguish URL between validation and other errors
class InvalidURL(Exception):
    pass

