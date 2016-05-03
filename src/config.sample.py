#!/usr/bin/env python
# -*- coding: utf-8 -*-
db_name=''

pushover_app_token=''
sia_base = 'https://www.sia.aviation-civile.gouv.fr/aip/enligne/Atlas-VAC/FR/'
sia_link_page = 'VACProduitPartie.htm'
sia_link_needle = 'Liste de contr'

pdf_dst = 'ctrl.pdf'
pdf_regex = "^(?P<ref>(?:AD 2 (?P<oaci1>LF[A-Z]{2})|AD-2\.VAC\.(?P<oaci2>LF[A-Z]{2})).*) (?P<date>[0-9]{2} (?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) [0-9]{4})$"
pdf_pages = (15, 30)
pdf_ad = (300, 600)
pdf_records = (1000, 2000)
