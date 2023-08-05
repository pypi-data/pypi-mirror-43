# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv1

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv1.decorators import lazy_property
from apimaticcalculatorpythonv1.configuration import Configuration
from apimaticcalculatorpythonv1.controllers.simple_calculator import SimpleCalculator


class Apimaticcalculatorpythonv1Client(object):

    config = Configuration

    @lazy_property
    def simple_calculator(self):
        return SimpleCalculator()


    def __init__(self,
                 gfdsfkl=None,
                 dsfsdf=None,
                 basic_auth_user_name=None,
                 basic_auth_password=None):
        if gfdsfkl != None:
            Configuration.gfdsfkl = gfdsfkl
        if dsfsdf != None:
            Configuration.dsfsdf = dsfsdf
        if basic_auth_user_name != None:
            Configuration.basic_auth_user_name = basic_auth_user_name
        if basic_auth_password != None:
            Configuration.basic_auth_password = basic_auth_password


