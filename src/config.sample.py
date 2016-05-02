#!/usr/bin/env python
# -*- coding: utf-8 -*-
pushover_app_token=''
sia_base = 'https://www.sia.aviation-civile.gouv.fr/aip/enligne/Atlas-VAC/FR/'
sia_link_page = 'VACProduitPartie.htm'
sia_link_needle = 'Liste de contr'

pdf_dst = 'ctrl.pdf'
pdf_regex = "^(?P<ref>(?:AD 2 |AD-2|CTL-[0-9]+|GEN VAC [A-Za-z0-9]+|SIV [A-Z]{3} [0-9]+).*) (?P<date>[0-9]{2} (?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) [0-9]{4})$"
pdf_min_pages = 15
pdf_min_records = 1200
