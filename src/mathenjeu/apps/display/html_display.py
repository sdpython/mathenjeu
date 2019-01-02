"""
@file
@brief Defines :epkg:`HTML` displays.
"""
from ...activities import Display


class DisplayQuestionChoiceHTML(Display):
    """
    Renders a question into :epkg:`HTML`.
    """

    def __init__(self):
        """
        constructor
        """
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
                       next_button=group.get_next(item),
                       image=act['content'].get("show", None))
        context['has_previous_button'] = context['previous_button'] is not None
        context['has_next_button'] = context['next_button'] is not None
        return context
