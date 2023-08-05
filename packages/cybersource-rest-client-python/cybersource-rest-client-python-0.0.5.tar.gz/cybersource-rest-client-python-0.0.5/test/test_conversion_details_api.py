# coding: utf-8

"""
    CyberSource Flex API

    Simple PAN tokenization service

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import CyberSource
from CyberSource.rest import ApiException
from CyberSource.apis.conversion_details_api import ConversionDetailsApi


class TestConversionDetailsApi(unittest.TestCase):
    """ ConversionDetailsApi unit test stubs """

    def setUp(self):
        self.api = CyberSource.apis.conversion_details_api.ConversionDetailsApi()

    def tearDown(self):
        pass

    def test_get_conversion_detail(self):
        """
        Test case for get_conversion_detail

        Get conversion detail transactions
        """
        pass


if __name__ == '__main__':
    unittest.main()
