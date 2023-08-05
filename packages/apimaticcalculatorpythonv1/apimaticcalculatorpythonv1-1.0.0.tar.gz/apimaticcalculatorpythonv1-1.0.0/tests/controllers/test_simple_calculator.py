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


class SimpleCalculatorTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(SimpleCalculatorTests, cls).setUpClass()
        cls.controller = cls.api_client.simple_calculator

    # Check if multiplication works
    def test_multiply(self):
        # Parameters for the API call
        operation = 'MULTIPLY'
        x = 4
        y = 5

        # Perform the API call through the SDK function
        result = self.controller.new_endpoint_it_is(operation, x, y)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        self.assertEqual('20', self.response_catcher.response.raw_body)


