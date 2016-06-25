#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mongoengine
from datetime import datetime

class ControlList(mongoengine.Document):
    date = mongoengine.DateTimeField(required=True, default=datetime.now)
    data = mongoengine.DictField(required=True)

    @staticmethod
    def computeDiff(old, new):
        oldKeys = set(old.keys())
        newKeys = set(new.keys())
        intersect = oldKeys.intersection(newKeys)
        mod = set(ad for ad in intersect if old[ad] != new[ad])

        adAdd = newKeys - oldKeys
        adDel = oldKeys - newKeys
        adMod = {}

        for ad in mod:
            adMod[ad] = {}

            oldPages = {a['ref'] : a['date'] for a in old[ad]}
            newPages = {a['ref'] : a['date'] for a in new[ad]}
            oldPagesKeys = set(oldPages.keys())
            newPagesKeys = set(newPages.keys())
            pagesInt = oldPagesKeys.intersection(newPagesKeys)

            adMod[ad]['add'] = newPagesKeys - oldPagesKeys
            adMod[ad]['del'] = oldPagesKeys - newPagesKeys
            adMod[ad]['mod'] = {p : (oldPages[p], newPages[p]) for p in pagesInt if oldPages[p] != newPages[p]}

        return adAdd, adMod, adDel
