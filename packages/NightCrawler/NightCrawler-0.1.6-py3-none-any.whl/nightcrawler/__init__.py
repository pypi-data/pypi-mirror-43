#!/bin/env python
# -*- coding: utf-8 -*-

# Author: Grzegorz Szczudlik
# Date: 02.03.19 18:04

import logging as logger

version = "0.1.6"
user_agent = "NightCrawler/%s" % version

logger.basicConfig(level=logger.WARN,
                   format='%(name)-12s: %(levelname)-8s %(message)s',
                   datefmt='%m-%d %H:%M')
