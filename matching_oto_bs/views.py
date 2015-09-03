# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Choice1(Page):

    form_model = models.Player
    form_fields = ['first_choice']

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'respondants_num': range(1, Constants.respondants_num+1),
            'common_ranks': self.session.vars['common_ranks'],
            'private_ranks': self.session.vars['prop_prefs'][self.player.id_in_group-1],
            'power': self.session.vars['power'][self.player.id_in_group-1],
        }


class Choice2(Page):

    form_model = models.Player
    form_fields = ['second_choice']

    def is_displayed(self):
        return self.player.matched == Constants.respondants_num

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'respondants_num': range(1, Constants.respondants_num+1),
            'players_num': range(1, Constants.players_per_group+1),
            'common_ranks': self.session.vars['common_ranks'],
            'private_ranks': self.session.vars['prop_prefs'][self.player.id_in_group-1],
            'power': self.session.vars['power'][self.player.id_in_group-1],
            'players': self.subsession.get_players,
            'match_pair': self.player.matched,
        }


class Choice3(Page):

    form_model = models.Player
    form_fields = ['third_choice']

    def is_displayed(self):
        return self.player.matched == Constants.respondants_num

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'respondants_num': range(1, Constants.respondants_num+1),
            'players_num': range(1, Constants.players_per_group+1),
            'common_ranks': self.session.vars['common_ranks'],
            'private_ranks': self.session.vars['prop_prefs'][self.player.id_in_group-1],
            'power': self.session.vars['power'][self.player.id_in_group-1],
            'players': self.subsession.get_players,
            'match_pair': self.player.matched,
        }


class ResultsWaitPage1(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs1()


class ResultsWaitPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs2()


class ResultsWaitPage3(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs3()


class NextRoundWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.before_session_starts()


class EachResults(Page):

    def is_displayed(self):
        return self.player.matched != Constants.respondants_num

    def vars_for_template(self):

        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'respondants_num': range(1, Constants.respondants_num+1),
            'players_num': range(1, Constants.players_per_group+1),
            'common_ranks': self.session.vars['common_ranks'],
            'private_ranks': self.session.vars['prop_prefs'][self.player.id_in_group-1],
            'power': self.session.vars['power'][self.player.id_in_group-1],
            'first_choice': self.player.first_choice,
            'second_choice': self.player.second_choice,
            'third_choice': self.player.third_choice,
            'players': self.subsession.get_players,
            'match_pair': self.player.matched,
            'payoff': self.player.payoff,
        }


class Results(Page):

    def vars_for_template(self):

        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'respondants_num': range(1, Constants.respondants_num+1),
            'players_num': range(1, Constants.players_per_group+1),
            'common_ranks': self.session.vars['common_ranks'],
            'private_ranks': self.session.vars['prop_prefs'][self.player.id_in_group-1],
            'power': self.session.vars['power'][self.player.id_in_group-1],
            'first_choice': self.player.first_choice,
            'second_choice': self.player.second_choice,
            'third_choice': self.player.third_choice,
            'players': self.subsession.get_players,
            'match_pair': self.player.matched,
            'payoff': self.player.payoff,
        }


class ResultsSummary(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
            'player_in_all_rounds': self.player.in_all_rounds(),
        }


page_sequence = [
    Choice1,
    ResultsWaitPage1,
    Choice2,
    EachResults,
    ResultsWaitPage2,
    Choice3,
    EachResults,
    ResultsWaitPage3,
    Results,
    NextRoundWaitPage,
    ResultsSummary
]
