"""
@file
@brief Starts an app locally to test it.
"""
from OpenSSL import crypto


def create_self_signed_cert(keyfile="key.pem", certfile="cert.pem",
                            country='FR', state='Paris', location='Paris',
                            organization='mathenjeu', cn='mathenjeu',
                            organizational_unit_name=None,
                            email=None, size=4096, days=365, algo="sha256",
                            fLOG=print):
    """
    Creates a signed certificate.

    @param      keyfile     key file
    @param      certfile    certificate file
    @param      country     country
    @param      state       state
    @param      location    location
    @param      cn          common name
    @param      organization organization
    @param      organizational_unit_name organizational unit name (can be empty)
    @param      email       email (can be empty)
    @param      size        key size
    @param      days        days it is valid
    @param      algo        algorithm
    @param      fLOG        logging function

    See also `How to generate a certificate using pyOpenSSL to make it secure connection?
    <https://stackoverflow.com/questions/44055029/how-to-generate-a-certificate-using-pyopenssl-to-make-it-secure-connection>`_,
    `How to serve HTTP/2 using Python
    <https://medium.com/python-pandemonium/how-to-serve-http-2-using-python-5e5bbd1e7ff1>`_.

    .. cmdref::
        :title: Creates a signed certificate
        :cmd: -m mathenjeu create_self_signed_cert --help

        The command line creates a certificate used later by
        a service such as :epkg:`hypercorn` or :epkg:`waitress`.
        Example::

            python -m mathenjeu create_self_signed_cert --keyfile=key.pem --certfile=cert.pem
    """
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, size)

    cert = crypto.X509()

    cert.get_subject().C = country
    cert.get_subject().ST = state
    cert.get_subject().L = location
    cert.get_subject().O = organization
    if organizational_unit_name:
        cert.get_subject().OU = organizational_unit_name
    cert.get_subject().CN = cn
    if email:
        cert.get_subject().emailAddress = email

    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(5 * days * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    with open(certfile, 'wb') as f:
        if fLOG:
            fLOG("[create_self_signed_cert] create '{0}'".format(certfile))
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    with open(keyfile, 'wb') as f:
        if fLOG:
            fLOG("[create_self_signed_cert] create '{0}'".format(keyfile))
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
