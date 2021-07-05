from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from statistics import mean

class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        user_agent = self.request.META['HTTP_USER_AGENT']
        is_mobile = False
        for substring in ['Mobi', 'Android']:
            if substring in user_agent:
                is_mobile = True
        self.participant.vars['is_mobile'] = is_mobile

class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

class QuizQuestions(Page):
    form_model = 'player'
    form_fields = ['quiz_answer']

    def is_displayed(self):
        return self.round_number == 1

    #def before_next_page(self):
    #    return self.player.evaluate_quiz()


class QuizAnswers(Page):
    def is_displayed(self):
        return self.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = []
    live_method = 'live_decision'

    def vars_for_template(self):
        return dict(
            first_number=self.participant.vars['numbers'][0][0],
            second_number=self.participant.vars['numbers'][0][1],
            turn=self.round_number
        )

    def before_next_page(self):
        return self.player.update_dataset()

# class Cross(Page):
#     def vars_for_template(self):
#         return dict(
#             turn=self.round_number
#         )

class Feedback(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['feedback']

    # def before_next_page(self):
    #     return self.player.update_dataset()

class Results(Page):
    # def is_displayed(self):
    #     return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return dict(
            accuracy=round(mean(self.participant.vars['responses_correct']) * 100, 2),
            accuracy_per=round(mean(self.participant.vars['responses_correct']), 2),
            speed=round(mean(self.participant.vars['responses_time']), 2),
        )

class Mobile(Page):
    def is_displayed(self):
        return self.participant.vars['is_mobile']

page_sequence = [Welcome, Mobile,
                 # Instructions, QuizQuestions, QuizAnswers,
                 # Cross,
                 Decision, Feedback, Results]
