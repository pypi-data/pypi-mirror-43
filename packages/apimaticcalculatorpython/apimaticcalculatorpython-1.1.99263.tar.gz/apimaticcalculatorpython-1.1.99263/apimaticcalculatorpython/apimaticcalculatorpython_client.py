# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpython

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpython.decorators import lazy_property
from apimaticcalculatorpython.configuration import Configuration
from apimaticcalculatorpython.controllers.calculator_e_ps import CalculatorEPs


class ApimaticcalculatorpythonClient(object):

    config = Configuration

    @lazy_property
    def calculator_e_ps(self):
        return CalculatorEPs()



