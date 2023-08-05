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
from CyberSource.apis.void_api import VoidApi


class TestVoidApi(unittest.TestCase):
    """ VoidApi unit test stubs """

    def setUp(self):
        self.api = CyberSource.apis.void_api.VoidApi()

    def tearDown(self):
        pass

    def test_void_capture(self):
        """
        Test case for void_capture

        Void a Capture
        """
        pass

    def test_void_credit(self):
        """
        Test case for void_credit

        Void a Credit
        """
        pass

    def test_void_payment(self):
        """
        Test case for void_payment

        Void a Payment
        """
        pass

    def test_void_refund(self):
        """
        Test case for void_refund

        Void a Refund
        """
        pass


if __name__ == '__main__':
    unittest.main()
