from .autologs import generate_logs
import logging
import pytest


@generate_logs()
def full_log(name, version='1', **kwargs):
    """
    Get version by name
    """
    return


def test1():
    full_log(name='test1')
