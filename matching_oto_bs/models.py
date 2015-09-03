# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import numpy as np
import matching_algo

import otree.models
import otree.constants
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Y.Ogawa'

doc = """
Matching Market Experiment with common value under incomplete information.
This is a one-to-one matching version.
"""


class Constants(BaseConstants):
    name_in_url = 'mamatching_oto_bs'
    players_per_group = 10
    num_rounds = 10
    respondants_num = 8


class Subsession(BaseSubsession):

    def before_session_starts(self):
        alpha = 0.3
        common_value = np.random.rand(Constants.respondants_num)
        private_value = np.random.rand(Constants.players_per_group, Constants.respondants_num)
        power = np.random.normal(50, 10, Constants.players_per_group).astype(np.int)

        common_ranks = np.argsort(common_value)[::-1]
        utility = np.zeros((Constants.players_per_group, Constants.respondants_num))
        prop_prefs = np.zeros((Constants.players_per_group, Constants.respondants_num), dtype=int)

        for prop_id in range(Constants.players_per_group):
            for resp_id in range(Constants.respondants_num):
                utility[prop_id][resp_id] = \
                    alpha * common_value[resp_id] + \
                    (1 - alpha) * private_value[prop_id][resp_id]
        for prop_id in range(Constants.players_per_group):
            prop_prefs[prop_id] = np.argsort(utility[prop_id])[::-1]
        self.session.vars['common_ranks'] = common_ranks
        self.session.vars['prop_prefs'] = prop_prefs
        self.session.vars['power'] = power


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoffs1(self):
        submit_prefs = np.zeros(Constants.players_per_group, dtype=int)
        for p in self.get_players():
            submit_prefs[p.id_in_group-1] = p.first_choice

        resp_rest = np.ones(Constants.respondants_num, dtype=int)

        matching = matching_algo.matching_oto_bs(submit_prefs, resp_rest, self.session.vars['power'])

        for p in self.get_players():
            p.matched = matching[p.id_in_group-1]
            if matching[p.id_in_group-1] != Constants.respondants_num:
                p.payoff = np.where(self.session.vars['prop_prefs'][p.id_in_group-1][::-1] == matching[p.id_in_group-1])[0][0] + 1
            else:
                p.payoff = 0

    def set_payoffs2(self):
        submit_prefs = np.zeros(Constants.players_per_group, dtype=int)
        for p in self.get_players():
            if p.matched == Constants.respondants_num:
                submit_prefs[p.id_in_group-1] = p.second_choice
            else:
                submit_prefs[p.id_in_group-1] = Constants.respondants_num

        resp_rest = np.ones(Constants.respondants_num, dtype=int)
        for p in self.get_players():
            if p.matched != Constants.respondants_num:
                resp_rest[p.matched] -= 1

        matching = matching_algo.matching_oto_bs(submit_prefs, resp_rest, self.session.vars['power'])

        for p in self.get_players():
            if p.matched == Constants.respondants_num:
                p.matched = matching[p.id_in_group-1]
                if matching[p.id_in_group-1] != Constants.respondants_num:
                    p.payoff = \
                    np.where(self.session.vars['prop_prefs'][p.id_in_group-1][::-1] == matching[p.id_in_group-1])[0][0] + 1

    def set_payoffs3(self):
        submit_prefs = np.zeros(Constants.players_per_group, dtype=int)
        for p in self.get_players():
            if p.matched == Constants.respondants_num:
                submit_prefs[p.id_in_group-1] = p.third_choice
            else:
                submit_prefs[p.id_in_group-1] = Constants.respondants_num

        resp_rest = np.ones(Constants.respondants_num, dtype=int)
        for p in self.get_players():
            if p.matched != Constants.respondants_num:
                resp_rest[p.matched] -= 1

        matching = matching_algo.matching_oto_bs(submit_prefs, resp_rest, self.session.vars['power'])

        for p in self.get_players():
            if p.matched == Constants.respondants_num:
                p.matched = matching[p.id_in_group-1]
                if matching[p.id_in_group-1] != Constants.respondants_num:
                    p.payoff = \
                    np.where(self.session.vars['prop_prefs'][p.id_in_group-1][::-1] == matching[p.id_in_group-1])[0][0] + 1


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    first_choice = models.PositiveIntegerField(min=0, max=Constants.respondants_num-1)
    second_choice = models.PositiveIntegerField(min=0, max=Constants.respondants_num-1)
    third_choice = models.PositiveIntegerField(min=0, max=Constants.respondants_num-1)

    matched = models.PositiveIntegerField(min=0, max=Constants.respondants_num)
