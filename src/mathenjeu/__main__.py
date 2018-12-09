# -*- coding: utf-8 -*-
"""
@file
@brief Implements command line ``python -m mathenjeu <command> <args>``.
"""
import sys
from pyquickhelper.cli import cli_main_helper


def main(args, fLOG=print):
    """
    Implements ``python -m mathenjeu <command> <args>``.

    @param      args        command line arguments
    @param      fLOG        logging function
    """
    try:
        from .cli import create_local_app
    except ImportError:
        from mathenjeu.cli import create_local_app

    fcts = dict(local_webapp=create_local_app)
    cli_main_helper(fcts, args=args, fLOG=fLOG)


if __name__ == "__main__":
    main(sys.argv[1:])
