# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv1

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv1.decorators import lazy_property
from apimaticcalculatorpythonv1.configuration import Configuration
from apimaticcalculatorpythonv1.controllers.calculator_e_ps import CalculatorEPs


class Apimaticcalculatorpythonv1Client(object):

    config = Configuration

    @lazy_property
    def calculator_e_ps(self):
        return CalculatorEPs()



