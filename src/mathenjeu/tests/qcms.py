# -*- coding: utf-8 -*-
"""
@file
@brief Shortcut to *tests*.
"""
from ..activities import Notion, QuestionChoice, HTMLForm, ActivityGroup


def simple_french_qcm():
    """
    Builds a simple French :epkg:`QCM`.
    """
    form = HTMLForm()
    math_sixieme = Notion('not-math-1', 'not-math-1', 'fr',
                          domain='maths', level='6A')

    objs = [
        QuestionChoice('ch1', '2prem', 'fr', 'Le nombre 2 est-il un nombre premier ?',
                       notion=math_sixieme, display=form,
                       answers=['Oui', 'Non', 'Je ne sais pas'],
                       expected_answers=['Oui']),
        QuestionChoice('ch2', '2prem', 'fr', 'Quelle est la surface d\'un cercle en fonction du rayon R ?',
                       notion=math_sixieme, display=form,
                       answers=['$\\pi R$', '$2 \\pi R$',
                                '$\\pi R^2$', '$\\pi^2 R^2$', '$3R^2/4$'],
                       expected_answers=['$\\pi R^2$']),
    ]
    return ActivityGroup("test_qcm1", "test_qcm1", objs)
