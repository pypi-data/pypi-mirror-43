# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv3

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv3.decorators import lazy_property
from apimaticcalculatorpythonv3.configuration import Configuration
from apimaticcalculatorpythonv3.controllers.calculator_endpoints import CalculatorEndpoints


class Apimaticcalculatorpythonv3Client(object):

    config = Configuration

    @lazy_property
    def calculator_endpoints(self):
        return CalculatorEndpoints()



