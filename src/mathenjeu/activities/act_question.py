# -*- coding: utf-8 -*-
"""
@file
@brief Base classes.
"""

from .base_classes import Activity, Display


class HTMLForm(Display):
    """
    Displays a question as one HTML form.
    """

    def __init__(self):
        Display.__init__(self, 'disp_q1', 'disp_q1')


class QuestionChoice(Activity):
    """
    Defines a question with multiple choices.
    """

    def __init__(self, eid, name, lang, title, notion=None,
                 display=None, description=None, answers=None,
                 expected_answers=None):
        """
        @param      eid                 identifier
        @param      name                unique name
        @param      lang                language
        @param      title               display name
        @param      notion              notion (@see cl Notion)
        @param      display             display (@see cl Display)
        @param      description         description
        @param      answers             answers (dictionary ``{ code, display }``)
        @param      expected_answers    expected_answers, list of codes
        """
        if isinstance(answers, list):
            answers = {k: k for k in answers}
        if not isinstance(answers, dict):
            raise TypeError("answers must be a dictionary")
        if not isinstance(expected_answers, list):
            raise TypeError("expected_answers must be a list")
        for exp in expected_answers:
            if exp not in answers:
                raise ValueError(
                    "One expected answer '{0}' is unknwon.".format(exp))
        Activity.__init__(self, eid, name, lang, title, notion=notion,
                          display=display, description=description,
                          content=dict(answers=answers, expected_answers=expected_answers))

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
