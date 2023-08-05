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


class PtsV2PaymentsPost201ResponsePaymentInformation(object):
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
        'card': 'PtsV2PaymentsPost201ResponsePaymentInformationCard',
        'tokenized_card': 'PtsV2PaymentsPost201ResponsePaymentInformationTokenizedCard',
        'account_features': 'PtsV2PaymentsPost201ResponsePaymentInformationAccountFeatures',
        'bank': 'PtsV2PaymentsPost201ResponsePaymentInformationBank'
    }

    attribute_map = {
        'card': 'card',
        'tokenized_card': 'tokenizedCard',
        'account_features': 'accountFeatures',
        'bank': 'bank'
    }

    def __init__(self, card=None, tokenized_card=None, account_features=None, bank=None):
        """
        PtsV2PaymentsPost201ResponsePaymentInformation - a model defined in Swagger
        """

        self._card = None
        self._tokenized_card = None
        self._account_features = None
        self._bank = None

        if card is not None:
          self.card = card
        if tokenized_card is not None:
          self.tokenized_card = tokenized_card
        if account_features is not None:
          self.account_features = account_features
        if bank is not None:
          self.bank = bank

    @property
    def card(self):
        """
        Gets the card of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :return: The card of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :rtype: PtsV2PaymentsPost201ResponsePaymentInformationCard
        """
        return self._card

    @card.setter
    def card(self, card):
        """
        Sets the card of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :param card: The card of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :type: PtsV2PaymentsPost201ResponsePaymentInformationCard
        """

        self._card = card

    @property
    def tokenized_card(self):
        """
        Gets the tokenized_card of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :return: The tokenized_card of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :rtype: PtsV2PaymentsPost201ResponsePaymentInformationTokenizedCard
        """
        return self._tokenized_card

    @tokenized_card.setter
    def tokenized_card(self, tokenized_card):
        """
        Sets the tokenized_card of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :param tokenized_card: The tokenized_card of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :type: PtsV2PaymentsPost201ResponsePaymentInformationTokenizedCard
        """

        self._tokenized_card = tokenized_card

    @property
    def account_features(self):
        """
        Gets the account_features of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :return: The account_features of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :rtype: PtsV2PaymentsPost201ResponsePaymentInformationAccountFeatures
        """
        return self._account_features

    @account_features.setter
    def account_features(self, account_features):
        """
        Sets the account_features of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :param account_features: The account_features of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :type: PtsV2PaymentsPost201ResponsePaymentInformationAccountFeatures
        """

        self._account_features = account_features

    @property
    def bank(self):
        """
        Gets the bank of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :return: The bank of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :rtype: PtsV2PaymentsPost201ResponsePaymentInformationBank
        """
        return self._bank

    @bank.setter
    def bank(self, bank):
        """
        Sets the bank of this PtsV2PaymentsPost201ResponsePaymentInformation.

        :param bank: The bank of this PtsV2PaymentsPost201ResponsePaymentInformation.
        :type: PtsV2PaymentsPost201ResponsePaymentInformationBank
        """

        self._bank = bank

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
        if not isinstance(other, PtsV2PaymentsPost201ResponsePaymentInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
