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


class PtsV2CreditsPost201ResponseProcessingInformationBankTransferOptions(object):
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
        'settlement_method': 'str'
    }

    attribute_map = {
        'settlement_method': 'settlementMethod'
    }

    def __init__(self, settlement_method=None):
        """
        PtsV2CreditsPost201ResponseProcessingInformationBankTransferOptions - a model defined in Swagger
        """

        self._settlement_method = None

        if settlement_method is not None:
          self.settlement_method = settlement_method

    @property
    def settlement_method(self):
        """
        Gets the settlement_method of this PtsV2CreditsPost201ResponseProcessingInformationBankTransferOptions.
        Method used for settlement.  Possible values: - **A**: Automated Clearing House (default for credits and for transactions using Canadian dollars) - **F**: Facsimile draft (U.S. dollars only) - **B**: Best possible (U.S. dollars only) (default if the field has not already been configured for your merchant ID)  See \"Settlement Delivery Methods,\" page 44. 

        :return: The settlement_method of this PtsV2CreditsPost201ResponseProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._settlement_method

    @settlement_method.setter
    def settlement_method(self, settlement_method):
        """
        Sets the settlement_method of this PtsV2CreditsPost201ResponseProcessingInformationBankTransferOptions.
        Method used for settlement.  Possible values: - **A**: Automated Clearing House (default for credits and for transactions using Canadian dollars) - **F**: Facsimile draft (U.S. dollars only) - **B**: Best possible (U.S. dollars only) (default if the field has not already been configured for your merchant ID)  See \"Settlement Delivery Methods,\" page 44. 

        :param settlement_method: The settlement_method of this PtsV2CreditsPost201ResponseProcessingInformationBankTransferOptions.
        :type: str
        """
        if settlement_method is not None and len(settlement_method) > 1:
            raise ValueError("Invalid value for `settlement_method`, length must be less than or equal to `1`")

        self._settlement_method = settlement_method

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
        if not isinstance(other, PtsV2CreditsPost201ResponseProcessingInformationBankTransferOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
