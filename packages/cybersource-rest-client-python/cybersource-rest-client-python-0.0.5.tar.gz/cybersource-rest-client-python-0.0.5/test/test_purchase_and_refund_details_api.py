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
from CyberSource.apis.purchase_and_refund_details_api import PurchaseAndRefundDetailsApi


class TestPurchaseAndRefundDetailsApi(unittest.TestCase):
    """ PurchaseAndRefundDetailsApi unit test stubs """

    def setUp(self):
        self.api = CyberSource.apis.purchase_and_refund_details_api.PurchaseAndRefundDetailsApi()

    def tearDown(self):
        pass

    def test_get_purchase_and_refund_details(self):
        """
        Test case for get_purchase_and_refund_details

        Get Purchase and Refund details
        """
        pass


if __name__ == '__main__':
    unittest.main()
