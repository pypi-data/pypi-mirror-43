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


class Ptsv2paymentsClientReferenceInformationPartner(object):
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
        'original_transaction_id': 'str',
        'developer_id': 'str',
        'solution_id': 'str'
    }

    attribute_map = {
        'original_transaction_id': 'originalTransactionId',
        'developer_id': 'developerId',
        'solution_id': 'solutionId'
    }

    def __init__(self, original_transaction_id=None, developer_id=None, solution_id=None):
        """
        Ptsv2paymentsClientReferenceInformationPartner - a model defined in Swagger
        """

        self._original_transaction_id = None
        self._developer_id = None
        self._solution_id = None

        if original_transaction_id is not None:
          self.original_transaction_id = original_transaction_id
        if developer_id is not None:
          self.developer_id = developer_id
        if solution_id is not None:
          self.solution_id = solution_id

    @property
    def original_transaction_id(self):
        """
        Gets the original_transaction_id of this Ptsv2paymentsClientReferenceInformationPartner.
        Value that links the previous transaction to the current follow-on request. This value is assigned by the client software that is installed on the POS terminal, which makes it available to the terminal’s software and to CyberSource. Therefore, you can use this value to reconcile transactions between CyberSource and the terminal’s software.  CyberSource does not forward this value to the processor. Instead, the value is forwarded to the CyberSource reporting functionality.  This field is supported only on American Express Direct, FDC Nashville Global, and SIX. 

        :return: The original_transaction_id of this Ptsv2paymentsClientReferenceInformationPartner.
        :rtype: str
        """
        return self._original_transaction_id

    @original_transaction_id.setter
    def original_transaction_id(self, original_transaction_id):
        """
        Sets the original_transaction_id of this Ptsv2paymentsClientReferenceInformationPartner.
        Value that links the previous transaction to the current follow-on request. This value is assigned by the client software that is installed on the POS terminal, which makes it available to the terminal’s software and to CyberSource. Therefore, you can use this value to reconcile transactions between CyberSource and the terminal’s software.  CyberSource does not forward this value to the processor. Instead, the value is forwarded to the CyberSource reporting functionality.  This field is supported only on American Express Direct, FDC Nashville Global, and SIX. 

        :param original_transaction_id: The original_transaction_id of this Ptsv2paymentsClientReferenceInformationPartner.
        :type: str
        """
        if original_transaction_id is not None and len(original_transaction_id) > 32:
            raise ValueError("Invalid value for `original_transaction_id`, length must be less than or equal to `32`")

        self._original_transaction_id = original_transaction_id

    @property
    def developer_id(self):
        """
        Gets the developer_id of this Ptsv2paymentsClientReferenceInformationPartner.
        Identifier for the developer that helped integrate a partner solution to CyberSource.  Send this value in all requests that are sent through the partner solutions built by that developer. CyberSource assigns the ID to the developer.  Note When you see a developer ID of 999 in reports, the developer ID that was submitted is incorrect. 

        :return: The developer_id of this Ptsv2paymentsClientReferenceInformationPartner.
        :rtype: str
        """
        return self._developer_id

    @developer_id.setter
    def developer_id(self, developer_id):
        """
        Sets the developer_id of this Ptsv2paymentsClientReferenceInformationPartner.
        Identifier for the developer that helped integrate a partner solution to CyberSource.  Send this value in all requests that are sent through the partner solutions built by that developer. CyberSource assigns the ID to the developer.  Note When you see a developer ID of 999 in reports, the developer ID that was submitted is incorrect. 

        :param developer_id: The developer_id of this Ptsv2paymentsClientReferenceInformationPartner.
        :type: str
        """
        if developer_id is not None and len(developer_id) > 8:
            raise ValueError("Invalid value for `developer_id`, length must be less than or equal to `8`")

        self._developer_id = developer_id

    @property
    def solution_id(self):
        """
        Gets the solution_id of this Ptsv2paymentsClientReferenceInformationPartner.
        Identifier for the partner that is integrated to CyberSource.  Send this value in all requests that are sent through the partner solution. CyberSource assigns the ID to the partner.  Note When you see a partner ID of 999 in reports, the partner ID that was submitted is incorrect. 

        :return: The solution_id of this Ptsv2paymentsClientReferenceInformationPartner.
        :rtype: str
        """
        return self._solution_id

    @solution_id.setter
    def solution_id(self, solution_id):
        """
        Sets the solution_id of this Ptsv2paymentsClientReferenceInformationPartner.
        Identifier for the partner that is integrated to CyberSource.  Send this value in all requests that are sent through the partner solution. CyberSource assigns the ID to the partner.  Note When you see a partner ID of 999 in reports, the partner ID that was submitted is incorrect. 

        :param solution_id: The solution_id of this Ptsv2paymentsClientReferenceInformationPartner.
        :type: str
        """
        if solution_id is not None and len(solution_id) > 8:
            raise ValueError("Invalid value for `solution_id`, length must be less than or equal to `8`")

        self._solution_id = solution_id

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
        if not isinstance(other, Ptsv2paymentsClientReferenceInformationPartner):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
