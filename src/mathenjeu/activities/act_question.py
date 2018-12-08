# -*- coding: utf-8 -*-
"""
@file
@brief Base classes.
"""
from collections import OrderedDict
from .base_classes import Activity


class QuestionChoice(Activity):
    """
    Defines a question with multiple choices.
    """

    def __init__(self, eid, name, lang, title, notion=None,
                 description=None, answers=None,
                 expected_answers=None, show=None):
        """
        @param      eid                 identifier
        @param      name                unique name
        @param      lang                language
        @param      title               display name
        @param      notion              notion (@see cl Notion)
        @param      description         description
        @param      answers             answers (dictionary ``{ code, display }``)
        @param      expected_answers    expected_answers, list of codes
        @param      show                one image to show
        """
        if not isinstance(expected_answers, list):
            raise TypeError("expected_answers must be a list")
        if isinstance(answers, list):
            ans = OrderedDict()
            for i, k in enumerate(answers):
                ans["a%d" % i] = k
            answers = ans
            rev = {v: k for k, v in answers.items()}
            expe = []
            for a in expected_answers:
                try:
                    v = rev[a]
                except KeyError:
                    raise KeyError("Unable to find '{0}' in {1}".format(
                        a, list(sorted(rev))))
                expe.append(v)
            expected_answers = expe
        elif isinstance(answers, dict):
            ans = OrderedDict()
            for i, k in enumerate(sorted(answers.items())):
                ans["a%d" % i] = k
            answers = ans
        elif not isinstance(answers, OrderedDict):
            raise TypeError("answers must be a of OrderedDict")
        for exp in expected_answers:
            if exp not in answers:
                raise ValueError(
                    "One expected answer '{0}' is unknown.".format(exp))
        content = dict(answers=answers,
                       expected_answers=expected_answers)
        if show:
            content['show'] = show
        Activity.__init__(self, eid, name, lang, title, notion=notion,
                          description=description, content=content)

    @property
    def Answers(self):
        """
        Returns the list of answers.
        """
        return self._col_content['answers']

    @property
    def ExpectedAnswers(self):
        """
        Returns the list of expected answers.
        """
        return self._col_content['expected_answers']
