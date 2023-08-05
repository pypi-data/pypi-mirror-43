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


class V1FileDetailsGet200ResponseLinksFiles(object):
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
        'file_id': 'str',
        'href': 'str',
        'method': 'str'
    }

    attribute_map = {
        'file_id': 'fileId',
        'href': 'href',
        'method': 'method'
    }

    def __init__(self, file_id=None, href=None, method=None):
        """
        V1FileDetailsGet200ResponseLinksFiles - a model defined in Swagger
        """

        self._file_id = None
        self._href = None
        self._method = None

        if file_id is not None:
          self.file_id = file_id
        if href is not None:
          self.href = href
        if method is not None:
          self.method = method

    @property
    def file_id(self):
        """
        Gets the file_id of this V1FileDetailsGet200ResponseLinksFiles.
        Unique identifier for each file

        :return: The file_id of this V1FileDetailsGet200ResponseLinksFiles.
        :rtype: str
        """
        return self._file_id

    @file_id.setter
    def file_id(self, file_id):
        """
        Sets the file_id of this V1FileDetailsGet200ResponseLinksFiles.
        Unique identifier for each file

        :param file_id: The file_id of this V1FileDetailsGet200ResponseLinksFiles.
        :type: str
        """

        self._file_id = file_id

    @property
    def href(self):
        """
        Gets the href of this V1FileDetailsGet200ResponseLinksFiles.

        :return: The href of this V1FileDetailsGet200ResponseLinksFiles.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this V1FileDetailsGet200ResponseLinksFiles.

        :param href: The href of this V1FileDetailsGet200ResponseLinksFiles.
        :type: str
        """

        self._href = href

    @property
    def method(self):
        """
        Gets the method of this V1FileDetailsGet200ResponseLinksFiles.

        :return: The method of this V1FileDetailsGet200ResponseLinksFiles.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """
        Sets the method of this V1FileDetailsGet200ResponseLinksFiles.

        :param method: The method of this V1FileDetailsGet200ResponseLinksFiles.
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
        if not isinstance(other, V1FileDetailsGet200ResponseLinksFiles):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
