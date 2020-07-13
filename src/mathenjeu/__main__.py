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
        from .cli import create_qcm_local_app, create_qcm_https_app, create_self_signed_cert
        from .cli import create_static_local_app, create_static_https_app
    except ImportError:  # pragma: no cover
        from mathenjeu.cli import create_qcm_local_app, create_qcm_https_app, create_self_signed_cert
        from mathenjeu.cli import create_static_local_app, create_static_https_app

    fcts = dict(qcm_local=create_qcm_local_app,
                qcm_https=create_qcm_https_app,
                static_local=create_static_local_app,
                static_https=create_static_https_app,
                create_self_signed_cert=create_self_signed_cert)
    cli_main_helper(fcts, args=args, fLOG=fLOG)


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
