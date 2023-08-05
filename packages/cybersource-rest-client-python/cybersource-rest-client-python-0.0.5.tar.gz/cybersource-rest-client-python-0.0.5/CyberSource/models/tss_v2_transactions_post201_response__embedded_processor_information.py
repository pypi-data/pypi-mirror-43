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


class TssV2TransactionsPost201ResponseEmbeddedProcessorInformation(object):
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
        'processor': 'TssV2TransactionsGet200ResponseProcessorInformationProcessor'
    }

    attribute_map = {
        'processor': 'processor'
    }

    def __init__(self, processor=None):
        """
        TssV2TransactionsPost201ResponseEmbeddedProcessorInformation - a model defined in Swagger
        """

        self._processor = None

        if processor is not None:
          self.processor = processor

    @property
    def processor(self):
        """
        Gets the processor of this TssV2TransactionsPost201ResponseEmbeddedProcessorInformation.

        :return: The processor of this TssV2TransactionsPost201ResponseEmbeddedProcessorInformation.
        :rtype: TssV2TransactionsGet200ResponseProcessorInformationProcessor
        """
        return self._processor

    @processor.setter
    def processor(self, processor):
        """
        Sets the processor of this TssV2TransactionsPost201ResponseEmbeddedProcessorInformation.

        :param processor: The processor of this TssV2TransactionsPost201ResponseEmbeddedProcessorInformation.
        :type: TssV2TransactionsGet200ResponseProcessorInformationProcessor
        """

        self._processor = processor

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
        if not isinstance(other, TssV2TransactionsPost201ResponseEmbeddedProcessorInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
