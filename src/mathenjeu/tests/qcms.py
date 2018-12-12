# -*- coding: utf-8 -*-
"""
@file
@brief Shortcut to *tests*.
"""
import math
from ..activities import Notion, QuestionChoice, ActivityGroup


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
        QuestionChoice('ch2', 'airecercle', 'fr', 'Quelle est la surface d\'un cercle en fonction du rayon R ?',
                       notion=math_sixieme,
                       answers=['$\\pi R$', '$2 \\pi R$',
                                '$\\pi R^2$', '$\\pi^2 R^2$', '$3R^2/4$'],
                       expected_answers=['$\\pi R^2$']),
        QuestionChoice('ch3', 'pen', 'fr', 'La figure est un pavage...',
                       notion=math_sixieme,
                       answers=['Impossible, aucune régularité.',
                                'Cela ne peut couvrir tout l\'espace.',
                                'Oui et j\'en connais l\'auteur.',
                                'C\'est un piège.'],
                       expected_answers=['Oui et j\'en connais l\'auteur.'],
                       show='static/img/pen.png'),
        QuestionChoice('ch4', 'peri', 'fr', 'La longueur des côtes françaises est de combien ?',
                       notion=math_sixieme,
                       answers=["%1.3fkm" % ((550000.e6 / math.pi)**0.5 * math.pi * 2 / 499),
                                'Il existe mais c\'est trop long à pied.',
                                'On ne sait pas le mesurer.',
                                'Sa longueur est infinie.',
                                "%1.3fkm" % ((550000.e6 / math.pi)**0.5 * math.pi * 2 / 1000), ],
                       expected_answers=['Sa longueur est infinie.'],
                       show='static/img/koch.png'),
        QuestionChoice('ch5', 'glace', 'fr', 'Un glaçon dans un verre fond. Le niveau de l\'eau monte-t-il ou descend-il ?',
                       notion=math_sixieme,
                       answers=['Il monte.', 'Il descend.', 'Il ne bouge pas.',
                                'Je n\'ai rien compris au réchauffement climatique.'],
                       expected_answers=['Il ne bouge pas.']),
        QuestionChoice('ch6', 'carre', 'fr', 'Un carré est un...',
                       notion=math_sixieme,
                       answers=['rectangle', 'parallélépidède', 'losange', 'un cercle',
                                'Je n\'ai rien compris au réchauffement climatique.'],
                       expected_answers=['rectangle', 'losange']),
        QuestionChoice('ch7', 'tva', 'fr', 'Vous avez acheté un produit à 10 euros. La TVA est à 20%, quelle est le prix sans la TVA ?',
                       notion=math_sixieme,
                       answers=['8 euros', '9.2', '10 * 0.8', '10 / 1.2', '7.8',
                                '10 / 1.2'],
                       expected_answers=['10 / 1.2']),
        QuestionChoice('ch8', 'dalton', 'fr', 'Gilles et Jean sont demi-frères, Jean et Charles sont demi-frères. Gilles et Charles sont...',
                       notion=math_sixieme,
                       answers=['frères, demi-frères',
                                'rien du tout', 'on ne sait pas'],
                       expected_answers=['on ne sait pas']),
        QuestionChoice('ch9', 'zoo', 'fr', 'Quel est le théorème de maths qui a servi à mesurer les Pyramides ?',
                       notion=math_sixieme,
                       answers=None,
                       expected_answers=['Thalès']),
    ]
    return ActivityGroup("simple_french_qcm", "simple_french_qcm", objs)
