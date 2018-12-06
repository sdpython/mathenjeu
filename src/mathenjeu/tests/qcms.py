# -*- coding: utf-8 -*-
"""
@file
@brief Shortcut to *tests*.
"""
from ..activities import Notion, QuestionChoice, ActivityGroup, Display


def simple_french_qcm():
    """
    Builds a simple French :epkg:`QCM`.
    """
    math_sixieme = Notion('not-math-1', 'not-math-1', 'fr',
                          domain='maths', level='6A')

    objs = [
        QuestionChoice('ch1', '2prem', 'fr', 'Le nombre 2 est-il un nombre premier ?',
                       notion=math_sixieme,
                       answers=['Oui', 'Non', 'Je ne sais pas'],
                       expected_answers=['Oui']),
        QuestionChoice('ch2', '2prem', 'fr', 'Quelle est la surface d\'un cercle en fonction du rayon R ?',
                       notion=math_sixieme,
                       answers=['$\\pi R$', '$2 \\pi R$',
                                '$\\pi R^2$', '$\\pi^2 R^2$', '$3R^2/4$'],
                       expected_answers=['$\\pi R^2$']),
    ]
    return ActivityGroup("test_qcm1", "test_qcm1", objs)


class DisplayQuestionChoiceHTML(Display):
    """
    Renders a question into HTML.
    """

    def __init__(self):
        Display.__init__(self, "qcm_html1", self.__class__.__name__)

    def get_context(self, group, item):
        """
        Renders a question specified as QCM.

        @param      group   group of activities, see @see cl ActivityGroup
        @param      item    item in the group
        @return             dictionary
        """
        act = group[item]
        context = dict(question=act['title'], description=act['description'],
                       answers=act['content']["answers"],
                       number=group.get_display_item(item),
                       nbnumber=len(group), qn=item,
                       previous_button=group.get_previous(item),
                       next_button=group.get_next(item))
        context['has_previous_button'] = context['previous_button'] is not None
        context['has_next_button'] = context['next_button'] is not None
        return context
