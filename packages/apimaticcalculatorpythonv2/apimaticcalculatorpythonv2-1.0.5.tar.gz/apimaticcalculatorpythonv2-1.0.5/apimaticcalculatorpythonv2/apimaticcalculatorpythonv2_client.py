# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv2

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv2.decorators import lazy_property
from apimaticcalculatorpythonv2.configuration import Configuration
from apimaticcalculatorpythonv2.controllers.calculator_e_ps import CalculatorEPs


class Apimaticcalculatorpythonv2Client(object):

    config = Configuration

    @lazy_property
    def calculator_e_ps(self):
        return CalculatorEPs()



