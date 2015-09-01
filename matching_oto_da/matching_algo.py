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

def matching(submit_prefs, power, resp_num):
    """
    Parameters
    ----------
    submit_prefs: array_like(int, ndim=2)
    power: array_like(int, ndim=1)
    resp_num: scalar(int)
    """
    submit_prefs = np.asarray(submit_prefs)
    prop_num = submit_prefs.shape[0]
    prop_matched = [resp_num for i in range(prop_num)]
    resp_matched = [prop_num for i in range(resp_num)]
    prop_approach = [0 for i in range(prop_num)]
    single = range(prop_num)

    while len(single) > 0:
        single_copy = [i for i in single]
        for prop_id in single_copy:
            if prop_approach[prop_id] >= submit_prefs.shape[1]:
                single.remove(prop_id)
                continue
            resp_id = submit_prefs[prop_id][prop_approach[prop_id]]
            prop_approach[prop_id] += 1
            if resp_matched[resp_id] == prop_num:
                single.remove(prop_id)
                prop_matched[prop_id] = resp_id
                resp_matched[resp_id] = prop_id
            else:
                if power[prop_id] > power[resp_matched[resp_id]]:
                    single.append(resp_matched[resp_id])
                    single.remove(prop_id)
                    prop_matched[prop_id] = resp_id
                    prop_matched[resp_matched[resp_id]] = resp_num
                    resp_matched[resp_id] = prop_id
    return prop_matched
