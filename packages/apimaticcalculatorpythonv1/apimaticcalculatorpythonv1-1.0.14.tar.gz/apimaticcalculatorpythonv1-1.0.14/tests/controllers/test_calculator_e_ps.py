# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv1

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from apimaticcalculatorpythonv1.api_helper import APIHelper


class CalculatorEPsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(CalculatorEPsTests, cls).setUpClass()
        cls.controller = cls.api_client.calculator_e_ps

    # Todo: Add description for test test_sum
    def test_sum(self):
        # Parameters for the API call
        operation = 'SUM'
        x = 5
        y = 20

        # Perform the API call through the SDK function
        result = self.controller.calculate(operation, x, y)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        self.assertEqual('25', self.response_catcher.response.raw_body)


    # Todo: Add description for test test_subtract
    def test_subtract(self):
        # Parameters for the API call
        operation = 'SUBTRACT'
        x = 20
        y = 5

        # Perform the API call through the SDK function
        result = self.controller.calculate(operation, x, y)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        self.assertEqual('15', self.response_catcher.response.raw_body)


    # Todo: Add description for test test_divide
    def test_divide(self):
        # Parameters for the API call
        operation = 'DIVIDE'
        x = 20
        y = 4

        # Perform the API call through the SDK function
        result = self.controller.calculate(operation, x, y)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        self.assertEqual('5', self.response_catcher.response.raw_body)


