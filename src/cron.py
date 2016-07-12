#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, mongoengine, config, sia, sys
from model.control_list import ControlList
from model.user import User

def _gen_msg(user, adNew, adMod, adDel):
    msg = ''
    if len(adNew):
        msg += "%s has been added\n" % (ad)

    if len(adDel):
        msg += "%s has been removed\n" % (ad)

    for ad in user.subscribedAd:
        if ad in adMod:
            msg += "%s has been updated:\n" % (ad)
            if len(adMod[ad]['add']):
                msg += "  New pages:\n"
                for page in adMod[ad]['add']:
                    msg += "    %s\n" % (page)

            if len(adMod[ad]['mod']):
                msg += "  Updated pages:\n"
                for page, dates in adMod[ad]['mod'].iteritems():
                    msg += "    %s (%s -> %s)\n" % (page, dates[0], dates[1])

            if len(adMod[ad]['del']):
                msg += "  Removed pages:\n"
                for page in adMod[ad]['del']:
                    msg += "    %s\n" % (page)
    return msg


def main():
    logging.basicConfig(level=logging.WARNING)
    db = mongoengine.connect(config.db_name)

    latest = ControlList.objects.order_by('-date').first()
    new = sia.parse_ctrl_list()
    if not new:
        logging.error("An error occurred when fetching control list data.")
        sys.exit(1)

    cl = ControlList(data=new)
    cl.save()

    if not latest:
        logging.warning("No previous Control list. Will notify users next time.")
        return

    adNew, adMod, adDel = ControlList.computeDiff(latest.data, cl.data)

    users = User.objects
    for user in users:
        msg = _gen_msg(user, adNew, adMod, adDel)
        user.notify("VAC Updates", msg)


if __name__ == '__main__':
    main()
