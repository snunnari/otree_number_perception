from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
#from user_agents import parse
from statistics import mean


class Name(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['name']

class Welcome(Page):

    def is_displayed(self):
        return self.round_number == 1

    #def before_next_page(self):
    #    user_agent = self.request.META['HTTP_USER_AGENT']
    #    is_mobile = False
    #    for substring in ['Mobi', 'Android']:
    #        if substring in user_agent:
    #            is_mobile = True
    #    self.participant.vars['is_mobile'] = is_mobile

        #user_agent = parse(user_agent)
        #is_safari = False
        # print(user_agent)

        #for substring in ['Safari']:
        #    if substring in str(user_agent):
        #        is_safari = True
        #        print('Participant is using Safari!')
        #    else:
        #        print('Participant is not using Safari')
        #self.participant.vars['is_safari'] = is_safari

class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1

class QuizQuestions(Page):

    form_model = 'player'
    form_fields = ['quiz_answer']

    def is_displayed(self):
        return self.round_number == 1

class QuizAnswers(Page):

    def is_displayed(self):
        return self.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = []
    live_method = 'live_decision'

    def vars_for_template(self):
        return dict(
            number=self.participant.vars['numbers'][0],
            turn=self.round_number
        )

    def before_next_page(self):
        return self.player.update_dataset()

class Cross(Page):

    def vars_for_template(self):
        return dict(
            turn=self.round_number
        )

#class Feedback(Page):
#    def is_displayed(self):
#        return self.round_number == Constants.num_rounds
#    form_model = 'player'
#    form_fields = ['feedback']

class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return dict(
            accuracy=round(mean(self.participant.vars['responses_correct']), 2) * 100,
            accuracy_per=round(mean(self.participant.vars['responses_correct']), 2),
            speed=round(mean(self.participant.vars['responses_time']), 2),
        )

#class Mobile(Page):
#
#    def is_displayed(self):
#        return self.participant.vars['is_mobile']


page_sequence = [Welcome,
                 Instructions, QuizQuestions, QuizAnswers,
                 #Cross,
                 Decision, Results]
