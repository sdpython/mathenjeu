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

    @staticmethod
    def _format_value(v):
        if isinstance(v, str):
            return "'{0}'".format(v.replace("\\", "\\\\").replace("'", "\\'"))
        else:
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
        self._col_eid = eid
        self._col_name = name
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
                 display=None, description=None, content=None):
        """
        @param      eid         identifier
        @param      name        unique name
        @param      lang        language
        @param      title       display name
        @param      notion      notion (@see cl Notion)
        @param      display     display (@see cl Display)
        @param      description description
        @param      content     content
        """
        LanguageBase.__init__(self, eid, name, lang)
        self._col_title = title
        self._col_notion = notion
        self._col_display = display
        self._col_description = description
        self._col_content = content
