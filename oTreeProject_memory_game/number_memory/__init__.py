from otree.api import *

import random
import time

class C(BaseConstants):
    NAME_IN_URL = 'memory_game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10
    INITIAL_LENGTH = 3

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    number_to_remember = models.StringField()
    recalled_number = models.StringField()
    round_score = models.IntegerField(initial=0)
    display_length = models.IntegerField()
    response_time = models.FloatField()

# PAGES

class Intro(Page):
    def is_displayed(player):
        return player.round_number == 1

    # template_name = 'Intro.html'

class DisplayNumber(Page):
    timeout_seconds = 3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['start_time'] = time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(number=player.number_to_remember)

    # template_name = 'DisplayNumber.html'

class Recall(Page):
    form_model = 'player'
    form_fields = ['recalled_number']
    # template_name = 'Recall.html'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        end_time = time.time()
        player.response_time = round(end_time - player.participant.vars['start_time'], 2)
        if player.recalled_number == player.number_to_remember:
            player.round_score = 1

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            correct=player.round_score == 1,
            original=player.number_to_remember,
            recalled=player.recalled_number,
            time=player.response_time,
        )

    # template_name = 'Results.html'

class FinalResults(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        total_score = sum(p.round_score for p in player.in_all_rounds())
        return dict(total_score=total_score, max_score=C.NUM_ROUNDS)

    # template_name = 'FinalResults.html'

# Helper function to generate number
def generate_number(length):
    return ''.join(random.choices('0123456789', k=length))

# Adaptive difficulty logic
def get_display_length(player: Player):
    base = C.INITIAL_LENGTH
    correct_streak = all(p.round_score == 1 for p in player.in_previous_rounds()[-3:])
    return base + player.round_number - 1 + (1 if correct_streak else 0)

def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        length = get_display_length(player)
        player.display_length = length
        player.number_to_remember = generate_number(length)

page_sequence = [Intro, DisplayNumber, Recall, Results, FinalResults]