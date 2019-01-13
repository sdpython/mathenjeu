"""
@file
@brief Shortcut to *cli*.
"""

from .qcm_app import create_qcm_https_app, create_qcm_local_app
from .static_app import create_static_https_app, create_static_local_app
from .openssl import create_self_signed_cert
