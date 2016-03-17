"""Gpiotest - gpiotest

.. moduleauthor:: Colin Alston <colin@praekelt.com>

"""

from gpiotest import service


def makeService(config):
    # Create GpiotestService
    return service.GpiotestService(config)
