#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config, urllib2
from bs4 import BeautifulSoup

def _sia_get_ctrl_list_url():
    ret = urllib2.urlopen(config.sia_base + config.sia_link_page)
    html = ret.read()
    soup = BeautifulSoup(html, "lxml")
    tags = soup.find_all('a')
    for tag in tags:
        if unicode(tag.string).startswith(config.sia_link_needle):
            return tag.get('href', None)
    return None
