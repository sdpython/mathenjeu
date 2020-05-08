"""
@file
@brief Helpers to interpet command line parameters.
"""
import os
import importlib
from ..tests import get_game


def name2activity(name):
    """
    Converts something like ``mathenjeu.tests.qcms.py:simple_french_qcm``
    into a class name. Calls function *simple_french_qcm*.

    :param name: name
    :return: result of simple_french_qcm

    It works if *name* contains ``':'`` otherwise
    it returns *name*.
    """
    if ':' in name:
        spl = name.split(':')
        modname = os.path.splitext(spl[0])[0]
        try:
            mod = importlib.import_module(modname)
        except ImportError as e:
            raise ImportError("Unable to import '{0}'".format(spl[0])) from e
        if not hasattr(mod, spl[1]):
            raise NameError(
                "Unable to find '{0}' in '{1}'".format(spl[1], spl[0]))
        return spl[1], getattr(mod, spl[1])()
    elif isinstance(name, str):
        raise TypeError("name '{0}' cannot be a string.".format(name))
    else:
        return name.__class__.__name__, name


def build_games(games, fct_game):
    """
    Interprets parameters.

    :param games: string
    :param fct_game: function which returns a game
        based on its name
    :return: modified *games*, *fct_game*
    """
    if isinstance(games, str) and fct_game is None:
        apps = [el.strip().split(',') for el in games.split(';')]
        games = {}
        games_obj = {}

        for k, n, p in apps:
            try:
                name, obj = name2activity(k)
                games[name] = (n, p)
                games_obj[name] = obj
            except TypeError:
                games[k] = (n, p)
                games_obj[k] = get_game(k)

        def get_games2(name):
            return games_obj[name]

        return games, get_games2
    else:
        return games, fct_game
