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
import csv

with open('numbers_high.csv', newline='') as numbers_high:
    data_high = csv.reader(numbers_high, delimiter=',', quotechar='|')
    data_vector_high = []
    for row in data_high:
        data_vector_high.append(row)

with open('numbers_low.csv', newline='') as numbers_low:
    data_low = csv.reader(numbers_low, delimiter=',', quotechar='|')
    data_vector_low = []
    for row in data_low:
        data_vector_low.append(row)

author = 'Your name here'

doc = """
Basic version of Discrimination Task
"""


class Constants(BaseConstants):
    name_in_url = 'one'
    players_per_group = None
    num_rounds = 1  # set to 1 in an App with live pages; Original: 150

    # number of iterations (equivalent of "num_rounds" for an App with live pages)
    num_iterations = 15  # Original: 150

    # cross duration in milliseconds
    cross_ms = 500

    # break duration in milliseconds
    break_ms = 5000

    #low = 31 # inclusive
    #high = 99 # inclusive
    threshold = 55

    # payoff = rate_accuracy * accuracy + rate_speed * speed
    rate_accuracy = 1.50
    rate_speed = 1.00

    # breaks = [51,101,151]
    # breaks = [5, 10]  # test
    breaks = [] # no pause
    # breaks = [math.ceil(num_iterations / 2) + 1]  # pause after 50% of total trials


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            # AMOUNTS FROM CSV #
            # N: to generate a new set of numbers, run script "generate_numbers.py" in project folder
            for p in self.get_players():
                if self.round_number == 1 and p.id_in_group % 2 == 1:
                    p.participant.vars['numbers'] = data_vector_high[int((p.id_in_group+1)/2-1)][:Constants.num_iterations]
                elif self.round_number == 1 and p.id_in_group % 2 == 0:
                    p.participant.vars['numbers'] = data_vector_low[int(p.id_in_group/2-1)][:Constants.num_iterations]

                # participant vars for live function
                p.participant.vars['responses'] = []
                p.participant.vars['responses_correct'] = []
                p.participant.vars['responses_time'] = []
                p.iteration = 0

                if p.id_in_group == 1:
                    print(p.participant.vars['numbers'])


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    name = models.StringField(label='')

    quiz_answer = models.StringField(
        choices=[['46', '46'], ['51', '51'], ['55', '55'], ['89', '89']],
        widget=widgets.RadioSelect,
        label=''''''
    )

    iteration = models.IntegerField()
    numbers = models.StringField()
    # higher = models.BooleanField()
    responses_correct = models.StringField()
    responses_time = models.StringField()

    feedback = models.LongStringField(label='', blank=True)

    def live_decision(self, data):
        # retrieve data from Decision.html (key pressed; correctness and time of decision)
        self.participant.vars['responses'].append(data[0])  # if needed!
        self.participant.vars['responses_correct'].append(data[1])
        self.participant.vars['responses_time'].append(data[2])
        self.iteration += 1

        # number to be displayed in Decision.html
        if self.iteration < Constants.num_iterations - 1:
            number = int(self.participant.vars['numbers'][self.iteration])
        else:
            number = int(self.participant.vars['numbers'][-1])

        response = dict(iteration=self.iteration, number=number)

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
        self.responses_correct = str(self.participant.vars['responses_correct'])
        self.responses_time = str(self.participant.vars['responses_time'])

        # set payoff
        self.payoff = c(Constants.rate_accuracy * round(mean(self.participant.vars['responses_correct']), 2) -
                        Constants.rate_speed * round(mean(self.participant.vars['responses_time']), 2))
