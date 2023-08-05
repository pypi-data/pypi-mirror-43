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


class PtsV2PaymentsPost201ResponseLinksSelf(object):
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
        'href': 'str',
        'method': 'str'
    }

    attribute_map = {
        'href': 'href',
        'method': 'method'
    }

    def __init__(self, href=None, method=None):
        """
        PtsV2PaymentsPost201ResponseLinksSelf - a model defined in Swagger
        """

        self._href = None
        self._method = None

        if href is not None:
          self.href = href
        if method is not None:
          self.method = method

    @property
    def href(self):
        """
        Gets the href of this PtsV2PaymentsPost201ResponseLinksSelf.
        URL

        :return: The href of this PtsV2PaymentsPost201ResponseLinksSelf.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this PtsV2PaymentsPost201ResponseLinksSelf.
        URL

        :param href: The href of this PtsV2PaymentsPost201ResponseLinksSelf.
        :type: str
        """

        self._href = href

    @property
    def method(self):
        """
        Gets the method of this PtsV2PaymentsPost201ResponseLinksSelf.
        HTTP method applied to above URL

        :return: The method of this PtsV2PaymentsPost201ResponseLinksSelf.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """
        Sets the method of this PtsV2PaymentsPost201ResponseLinksSelf.
        HTTP method applied to above URL

        :param method: The method of this PtsV2PaymentsPost201ResponseLinksSelf.
        :type: str
        """

        self._method = method

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
        if not isinstance(other, PtsV2PaymentsPost201ResponseLinksSelf):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
