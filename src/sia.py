#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config, urllib2, subprocess, re, logging
from bs4 import BeautifulSoup
from pyPdf import PdfFileReader
from pyPdf.utils import PdfReadError

def _get_ctrl_list_url():
    logging.info("Downloading initial SIA page")

    try:
        ret = urllib2.urlopen(config.sia_base + config.sia_link_page)
    except(urllib2.URLError):
        logging.error("An error occurred when downloading initial SIA page")
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
        logging.error("Could not extract Control List PDF URL")
        return False

    url = config.sia_base + url

    logging.info("Downloading Control List PDF")
    try:
        ret = urllib2.urlopen(url)
    except(urllib2.URLError):
        logging.info("An error occurred when downloading Control List PDF %s" % (url))
        return False

    f = open(config.pdf_dst, 'wb')
    f.write(ret.read())
    f.close()

    try:
        pdf = PdfFileReader(file(config.pdf_dst))
    except(IOError, PdfReadError):
        logging.info("An error occurred when attempting to open the PDF")
        return False

    if not config.pdf_pages[0] <= pdf.getNumPages() <= config.pdf_pages[1]:
        logging.info("PDF page number %d is out of range" % (pdf.getNumPages()))
        return False

    return True

def parse_ctrl_list():
    if not _dl_ctrl_list():
        logging.error("Could not retrieve Control List PDF")
        return False

    p = subprocess.Popen(["ps2ascii", config.pdf_dst], stdout=subprocess.PIPE)
    txt = p.communicate()[0]
    if p.returncode != 0:
        logging.error("Cound not convert PDF to text (ps2ascii returned %d)" % (p.returncode))
        return False

    r = re.compile(config.pdf_regex, flags=re.MULTILINE)
    found = r.findall(txt)

    if not config.pdf_records[0] <= len(found) <= config.pdf_records[1]:
        logging.error("Control List record number %d is out of range" % (len(found)))
        return False

    res = {}
    for ref, oaci1, oaci2, date in found:
        res.setdefault(oaci1 if oaci1 else oaci2, []).append({'ref': ref, 'date': date})

    if len(res) < config.pdf_ad[0] or len(res) > config.pdf_ad[1]:
        logging.error("Control List aerodromes number %d is out of range" % (len(res)))
        return False

    logging.info("Got %d aerodromes and %d entries" % (len(res), len(found)))

    return res
