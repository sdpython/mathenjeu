# -*- coding: utf-8 -*-
"""
@file
@brief Shortcut to *tests*.
"""

from .qcms import simple_french_qcm


def get_game(name):
    """
    Retrieves a game.

    @param      game        game
    @return                 game
    """
    if name == "test_qcm1":
        return simple_french_qcm()
    else:
        raise ValueError("Unknown game '{0}'".format(name))
