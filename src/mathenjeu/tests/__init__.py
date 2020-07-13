# -*- coding: utf-8 -*-
"""
@file
@brief Shortcut to *tests*.
"""

from .qcms import simple_french_qcm, ml_french_qcm


def get_game(name):
    """
    Retrieves a game.

    @param      name        game name
    @return                 game
    """
    if name in ("test_qcm1", "simple_french_qcm"):
        return simple_french_qcm()
    if name in ("test_ml1", "ml_french_qcm"):
        return ml_french_qcm()
    raise ValueError(  # pragma: no cover
        "Unknown game '{0}'".format(name))
