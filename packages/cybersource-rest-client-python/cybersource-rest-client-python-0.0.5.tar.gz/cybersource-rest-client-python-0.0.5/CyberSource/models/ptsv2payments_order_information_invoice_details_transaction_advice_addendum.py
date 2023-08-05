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


class Ptsv2paymentsOrderInformationInvoiceDetailsTransactionAdviceAddendum(object):
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
        'data': 'str'
    }

    attribute_map = {
        'data': 'data'
    }

    def __init__(self, data=None):
        """
        Ptsv2paymentsOrderInformationInvoiceDetailsTransactionAdviceAddendum - a model defined in Swagger
        """

        self._data = None

        if data is not None:
          self.data = data

    @property
    def data(self):
        """
        Gets the data of this Ptsv2paymentsOrderInformationInvoiceDetailsTransactionAdviceAddendum.
        Four Transaction Advice Addendum (TAA) fields. These fields are used to display descriptive information about a transaction on the customer’s American Express card statement. When you send TAA fields, start with amexdata_taa1, then ...taa2, and so on. Skipping a TAA field causes subsequent TAA fields to be ignored.  To use these fields, contact CyberSource Customer Support to have your account enabled for this feature. 

        :return: The data of this Ptsv2paymentsOrderInformationInvoiceDetailsTransactionAdviceAddendum.
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this Ptsv2paymentsOrderInformationInvoiceDetailsTransactionAdviceAddendum.
        Four Transaction Advice Addendum (TAA) fields. These fields are used to display descriptive information about a transaction on the customer’s American Express card statement. When you send TAA fields, start with amexdata_taa1, then ...taa2, and so on. Skipping a TAA field causes subsequent TAA fields to be ignored.  To use these fields, contact CyberSource Customer Support to have your account enabled for this feature. 

        :param data: The data of this Ptsv2paymentsOrderInformationInvoiceDetailsTransactionAdviceAddendum.
        :type: str
        """
        if data is not None and len(data) > 40:
            raise ValueError("Invalid value for `data`, length must be less than or equal to `40`")

        self._data = data

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
        if not isinstance(other, Ptsv2paymentsOrderInformationInvoiceDetailsTransactionAdviceAddendum):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
