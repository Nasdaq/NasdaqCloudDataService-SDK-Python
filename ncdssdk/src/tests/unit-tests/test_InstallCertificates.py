from ncdssdk.src.main.python.ncdsclient.internal.utils.InstallCertificates import InstallCertificates
from os import path, makedirs
import shutil


def test_install_at_default():
    install_cert = InstallCertificates()
    install_cert.install()

    assert path.exists('/tmp/ca.crt')


def test_install_at_existing_dir():
    p = './tmp/testDir'
    if not path.exists(p):
        makedirs(p)

    install_cert = InstallCertificates(p)
    install_cert.install()

    assert path.exists(p + '/ca.crt')


def test_install_at_non_existing_dir_and_file():
    p = './tmp/testDir'
    if path.exists(p):
        shutil.rmtree(p)

    install_cert = InstallCertificates(p)
    install_cert.install()

    assert path.exists(p + '/ca.crt')
