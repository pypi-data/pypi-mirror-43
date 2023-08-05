# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv2

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv2.decorators import lazy_property
from apimaticcalculatorpythonv2.configuration import Configuration
from apimaticcalculatorpythonv2.controllers.simple_calculator import SimpleCalculator


class Apimaticcalculatorpythonv2Client(object):

    config = Configuration

    @lazy_property
    def simple_calculator(self):
        return SimpleCalculator()



