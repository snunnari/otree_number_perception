from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random
from statistics import mean
import math

author = 'Your name here'

doc = """
Discrimination task with two numbers
"""


class Constants(BaseConstants):
    name_in_url = 'two'
    players_per_group = None
    num_rounds = 1

    # number of iterations (equivalent of "num_rounds" for an App with live pages)
    num_iterations = 150  # Original: 150

    # cross duration in milliseconds
    cross_ms = 500

    # break duration in milliseconds
    break_ms = 5000

    low = 11
    high = 99

    rate_accuracy = 1.5
    rate_speed = 1.0

    # breaks = [math.ceil(num_iterations/2) + 1]  # pause at half task; if empty, app will not pause
    breaks = []  # no pause

class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            p.iteration = 0

            if self.round_number == 1:
                numbers = []

                for iteration in range(Constants.num_iterations):
                    left_num = random.randint(Constants.low, Constants.high)
                    right_num = random.randint(Constants.low, Constants.high)

                    while left_num == right_num:
                        left_num = random.randint(Constants.low, Constants.high)
                        right_num = random.randint(Constants.low, Constants.high)

                    numbers.append([left_num, right_num])

                p.participant.vars['numbers'] = numbers
                p.participant.vars['responses'] = []
                p.participant.vars['responses_correct'] = []
                p.participant.vars['responses_time'] = []
                p.participant.vars['responses_correct_close'] = []
                p.participant.vars['responses_correct_far'] = []

                print(p.participant.vars['numbers'])

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    quiz_answer = models.StringField(
        choices=[['Q', 'Q'], ['A', 'A'], ['Z', 'Z'], ['?', '?']],
        widget=widgets.RadioSelect,
        label=''''''
    )

    iteration = models.IntegerField()
    numbers = models.StringField()
    # left_numbers = models.StringField()
    # right_numbers = models.StringField()
    # left_higher = models.BooleanField()
    responses = models.StringField()
    responses_correct = models.StringField()
    responses_time = models.StringField()
    feedback = models.LongStringField(label='', blank=True)

    def live_decision(self, data):
        # retrieve data from Decision.html (key pressed; correctness and time of decision)
        self.participant.vars['responses'].append(data[0])  # if needed!
        self.participant.vars['responses_correct'].append(data[1])
        self.participant.vars['responses_time'].append(data[2])
        self.iteration += 1

        # numbers to be displayed in Decision.html
        if self.iteration < Constants.num_iterations - 1:
            numbers = self.participant.vars['numbers'][self.iteration]
        else:
            numbers = self.participant.vars['numbers'][-1]

        response = dict(iteration=self.iteration, numbers=numbers)

        # print data for participant 1
        if self.id_in_group == 1:
            print(self.participant.vars['responses_correct'])
            # print(self.participant.vars['decisions_made'])
            print(self.participant.vars['responses_time'])
            print(response)

        return {self.id_in_group: response}

    # This function stores in the oTree dataset the decisions made (e.g., "['A', 'K', 'K',...]")
    # and numbers drawn at each round (e.g, "[50, 54, 54,...]"), both as strings.
    # It also computes the payoffs based on the player's performance
    def update_dataset(self):
        self.numbers = str(self.participant.vars['numbers'][:self.iteration])
        self.responses = str(self.participant.vars['responses'])
        self.responses_correct = str(self.participant.vars['responses_correct'])
        self.responses_time = str(self.participant.vars['responses_time'])

        # set payoff
        self.payoff = c(Constants.rate_accuracy * round(mean(self.participant.vars['responses_correct']), 2) -
                        Constants.rate_speed * round(mean(self.participant.vars['responses_time']), 2))
