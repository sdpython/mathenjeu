# -*- coding: utf-8 -*-
"""
@file
@brief Base classes.
"""


class Base:
    """
    Base class.
    """

    def __init__(self, eid, name):
        """
        @param      eid     entity id
        @param      name    unique name (mostly for logging)
        """
        self._col_eid = eid
        self._col_name = name

    @property
    def Id(self):
        """
        Returns the identifier.
        """
        return self._col_eid

    @property
    def Fields(self):
        """
        Returns all the fields.
        """
        return list(sorted(k for k in self.__dict__ if k.startswith("_col")))

    def to_dict(self):
        """
        Returns all values as a dictionary.
        """
        return {k: getattr(self, k) for k in self.__dict__ if k.startswith("_col")}

    @staticmethod
    def _format_value(v):
        if isinstance(v, str):
            return "'{0}'".format(v.replace("\\", "\\\\").replace("'", "\\'"))
        if isinstance(v, list):
            rs = [repr(_) for _ in v]
            return '[{0}]'.format(', '.join(rs))
        return repr(v)

    def __repr__(self):
        """
        Usual
        """
        name = self.__class__.__name__
        fields = self.Fields
        pars = ["{0}={1}".format(k, Base._format_value(
            getattr(self, k))) for k in fields]
        text = "{0}({1})".format(name, ", ".join(pars))
        return text

    def __getitem__(self, field):
        """
        Returns the value associated to a field.

        @param      field       field
        @return                 value
        """
        key = "_col_" + field
        if not hasattr(self, key):
            raise ValueError("Unable to find attribute '{0}'.".format(field))
        return getattr(self, key)


class Display(Base):
    """
    Defines how an activity should be displayed.
    """

    def __init__(self, eid, name):
        """
        @param  eid     unique identifier
        @param  name    name
        """
        Base.__init__(self, eid, name)


class LanguageBase(Base):
    """
    Base class for language specific content.
    """

    def __init__(self, eid, name, lang):
        """
        @param      eid     entity id
        @param      name    unique name (mostly for logging)
        @param      lang    language
        """
        Base.__init__(self, eid, name)
        self._col_lang = lang


class Notion(LanguageBase):
    """
    Defines what an activity intents to introduce.
    """

    def __init__(self, eid, name, lang, domain=None, level=None, depends=None,
                 content=None):
        """
        @param      eid     identifier
        @param      name    unique name
        @param      domain  domain (maths, ...)
        @param      lang    language
        @param      level   level, grade...
        @param      depends is there any needed notion to know before knowing this one?,
                            should be a list of @see cl Notion.
        @param      content data
        """
        if depends is not None and not isinstance(depends, list):
            depends = [depends]
        LanguageBase.__init__(self, eid, name, lang)
        self._col_domain = domain
        self._col_level = level
        self._col_depends = depends
        self._col_content = content


class Activity(LanguageBase):
    """
    Defines an activity, a question, a game...
    """

    def __init__(self, eid, name, lang, title, notion=None,
                 description=None, content=None):
        """
        @param      eid         identifier
        @param      name        unique name
        @param      lang        language
        @param      title       display name
        @param      notion      notion (@see cl Notion)
        @param      description description
        @param      content     content
        """
        LanguageBase.__init__(self, eid, name, lang)
        self._col_title = title
        self._col_notion = notion
        self._col_description = description
        self._col_content = content


class ActivityGroup(Base):
    """
    Defines a set of activities.
    """

    def __init__(self, eid, name, acts=None):
        """
        @param      eid         identifier
        @param      name        unique name
        @param      acts        set of activities
        """
        Base.__init__(self, eid, name)
        if acts is None:
            self._col_acts = []
        elif isinstance(acts, list):
            self._col_acts = acts
        else:
            raise TypeError("Activities must be defined as a list.")

    def __len__(self):
        """
        Returns the number of activities.
        """
        return len(self._col_acts)

    def __iter__(self):
        """
        To iterate on activities.
        """
        return self._col_acts.__iter__()

    def __getitem__(self, item):
        """
        Retrieves the question.

        @param      item        item
        @return                 @see cl Activity
        """
        if not isinstance(item, int):
            try:
                ii = int(item)
            except ValueError:
                raise ValueError(  # pylint: disable=W0707
                    "Unable to retrieve question '{0}'.".format(item))
        else:
            ii = item

        return self._col_acts[ii]

    def get_previous(self, current):
        """
        Computes the previous question or returns None
        if does not exist.

        @param      current     previous question
        @return                 next question or None
        """
        try:
            r = int(current)
        except ValueError:
            r = len(self)
        return (r - 1) if r > 0 else None

    def get_next(self, current):
        """
        Computes the next question or returns None
        if does not exist.

        @param      current     current question
        @return                 next question or None
        """
        try:
            r = int(current)
        except ValueError:
            r = len(self)
        return (r + 1) if r < len(self) - 1 else None

    def get_display_item(self, item):
        """
        Returns a displayable number.

        @param      item        item number
        @return                 string
        """
        if isinstance(item, int):
            return str(item + 1)  # items starts at 0
        elif isinstance(item, str):
            try:
                return self.get_display_item(int(item))
            except ValueError:
                return item
        else:
            raise TypeError("Unable to interpret '{0}'.".format(item))
