# coding: utf-8

"""
    CyberSource Flex API

    Simple PAN tokenization service

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class TssV2TransactionsGet200ResponseInstallmentInformation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'number_of_installments': 'str'
    }

    attribute_map = {
        'number_of_installments': 'numberOfInstallments'
    }

    def __init__(self, number_of_installments=None):
        """
        TssV2TransactionsGet200ResponseInstallmentInformation - a model defined in Swagger
        """

        self._number_of_installments = None

        if number_of_installments is not None:
          self.number_of_installments = number_of_installments

    @property
    def number_of_installments(self):
        """
        Gets the number_of_installments of this TssV2TransactionsGet200ResponseInstallmentInformation.
        Number of Installments.

        :return: The number_of_installments of this TssV2TransactionsGet200ResponseInstallmentInformation.
        :rtype: str
        """
        return self._number_of_installments

    @number_of_installments.setter
    def number_of_installments(self, number_of_installments):
        """
        Sets the number_of_installments of this TssV2TransactionsGet200ResponseInstallmentInformation.
        Number of Installments.

        :param number_of_installments: The number_of_installments of this TssV2TransactionsGet200ResponseInstallmentInformation.
        :type: str
        """

        self._number_of_installments = number_of_installments

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, TssV2TransactionsGet200ResponseInstallmentInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
