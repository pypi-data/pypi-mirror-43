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


class ErrorLinks(object):
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
        '_self': 'InlineResponseDefaultLinksNext',
        'documentation': 'list[InlineResponseDefaultLinksNext]',
        'next': 'list[InlineResponseDefaultLinksNext]'
    }

    attribute_map = {
        '_self': 'self',
        'documentation': 'documentation',
        'next': 'next'
    }

    def __init__(self, _self=None, documentation=None, next=None):
        """
        ErrorLinks - a model defined in Swagger
        """

        self.__self = None
        self._documentation = None
        self._next = None

        if _self is not None:
          self._self = _self
        if documentation is not None:
          self.documentation = documentation
        if next is not None:
          self.next = next

    @property
    def _self(self):
        """
        Gets the _self of this ErrorLinks.

        :return: The _self of this ErrorLinks.
        :rtype: InlineResponseDefaultLinksNext
        """
        return self.__self

    @_self.setter
    def _self(self, _self):
        """
        Sets the _self of this ErrorLinks.

        :param _self: The _self of this ErrorLinks.
        :type: InlineResponseDefaultLinksNext
        """

        self.__self = _self

    @property
    def documentation(self):
        """
        Gets the documentation of this ErrorLinks.

        :return: The documentation of this ErrorLinks.
        :rtype: list[InlineResponseDefaultLinksNext]
        """
        return self._documentation

    @documentation.setter
    def documentation(self, documentation):
        """
        Sets the documentation of this ErrorLinks.

        :param documentation: The documentation of this ErrorLinks.
        :type: list[InlineResponseDefaultLinksNext]
        """

        self._documentation = documentation

    @property
    def next(self):
        """
        Gets the next of this ErrorLinks.

        :return: The next of this ErrorLinks.
        :rtype: list[InlineResponseDefaultLinksNext]
        """
        return self._next

    @next.setter
    def next(self, next):
        """
        Sets the next of this ErrorLinks.

        :param next: The next of this ErrorLinks.
        :type: list[InlineResponseDefaultLinksNext]
        """

        self._next = next

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
        if not isinstance(other, ErrorLinks):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
