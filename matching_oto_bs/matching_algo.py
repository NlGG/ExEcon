# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import numpy as np
# </standard imports>

author = 'Y.Ogawa'

doc = """
Matching Algorithm For Matching Market Experiment.
This is a one-to-one matching version.
"""

def matching_oto_bs(submit_prefs, resp_rest, power):
    """
    Parameters
    ----------
    submit_prefs: array_like(int, ndim=1)
    resp_rest: array_like(int, ndim=1)
    power: array_like(int, ndim=1)
    """
    prop_num = submit_prefs.shape[0]
    resp_num = resp_rest.shape[0]
    prop_matched = [resp_num for i in range(prop_num)]
    resp_matched = [prop_num for i in range(resp_num)]

    for prop_id in range(prop_num):
        resp_id = submit_prefs[prop_id]
        if (resp_id != resp_num) and (resp_rest[resp_id] == 1):
            if resp_matched[resp_id] == prop_num:
                prop_matched[prop_id] = resp_id
                resp_matched[resp_id] = prop_id
            else:
                if power[prop_id] > power[resp_matched[resp_id]]:
                    prop_matched[prop_id] = resp_id
                    prop_matched[resp_matched[resp_id]] = resp_num
                    resp_matched[resp_id] = prop_id

    return prop_matched
