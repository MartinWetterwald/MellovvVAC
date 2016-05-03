#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config, urllib2, subprocess, re
from bs4 import BeautifulSoup
from pyPdf import PdfFileReader
from pyPdf.utils import PdfReadError

def _get_ctrl_list_url():
    try:
        ret = urllib2.urlopen(config.sia_base + config.sia_link_page)
    except(urllib2.URLError):
        return False

    soup = BeautifulSoup(ret.read(), "lxml")
    tags = soup.find_all('a')
    for tag in tags:
        if unicode(tag.string).startswith(config.sia_link_needle):
            return tag.get('href', None)

    return None

def _dl_ctrl_list():
    url = _get_ctrl_list_url()
    if not url:
        return False

    url = config.sia_base + url

    try:
        ret = urllib2.urlopen(url)
    except(urllib2.URLError):
        return False

    f = open(config.pdf_dst, 'wb')
    f.write(ret.read())
    f.close()

    try:
        pdf = PdfFileReader(file(config.pdf_dst))
    except(IOError, PdfReadError):
        return False

    if not config.pdf_pages[0] <= pdf.getNumPages() <= config.pdf_pages[1]:
        return False

    return True

def parse_ctrl_list():
    if not _dl_ctrl_list():
        return False

    p = subprocess.Popen(["ps2ascii", config.pdf_dst], stdout=subprocess.PIPE)
    txt = p.communicate()[0]
    if p.returncode != 0:
        return False

    r = re.compile(config.pdf_regex, flags=re.MULTILINE)
    found = r.findall(txt)

    if not config.pdf_records[0] <= len(found) <= config.pdf_records[1]:
        return False

    res = {}
    for ref, oaci1, oaci2, date in found:
        res.setdefault(oaci1 if oaci1 else oaci2, []).append({'ref': ref, 'date': date})

    if len(res) < config.pdf_ad[0] or len(res) > config.pdf_ad[1]:
        return False

    return res
