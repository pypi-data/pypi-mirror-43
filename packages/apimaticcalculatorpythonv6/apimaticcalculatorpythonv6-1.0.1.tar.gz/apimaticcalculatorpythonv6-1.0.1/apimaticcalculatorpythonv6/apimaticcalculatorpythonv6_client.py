# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv6

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv6.decorators import lazy_property
from apimaticcalculatorpythonv6.configuration import Configuration
from apimaticcalculatorpythonv6.controllers.calculator_endpoints import CalculatorEndpoints


class Apimaticcalculatorpythonv6Client(object):

    config = Configuration

    @lazy_property
    def calculator_endpoints(self):
        return CalculatorEndpoints()



