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


class Body3(object):
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
        'links': 'Tmsv1instrumentidentifiersLinks',
        'id': 'str',
        'object': 'str',
        'state': 'str',
        'bank_account': 'Tmsv1paymentinstrumentsBankAccount',
        'card': 'Tmsv1paymentinstrumentsCard',
        'buyer_information': 'Tmsv1paymentinstrumentsBuyerInformation',
        'bill_to': 'Tmsv1paymentinstrumentsBillTo',
        'processing_information': 'Tmsv1paymentinstrumentsProcessingInformation',
        'merchant_information': 'Tmsv1paymentinstrumentsMerchantInformation',
        'meta_data': 'Tmsv1instrumentidentifiersMetadata',
        'instrument_identifier': 'Tmsv1paymentinstrumentsInstrumentIdentifier'
    }

    attribute_map = {
        'links': '_links',
        'id': 'id',
        'object': 'object',
        'state': 'state',
        'bank_account': 'bankAccount',
        'card': 'card',
        'buyer_information': 'buyerInformation',
        'bill_to': 'billTo',
        'processing_information': 'processingInformation',
        'merchant_information': 'merchantInformation',
        'meta_data': 'metaData',
        'instrument_identifier': 'instrumentIdentifier'
    }

    def __init__(self, links=None, id=None, object=None, state=None, bank_account=None, card=None, buyer_information=None, bill_to=None, processing_information=None, merchant_information=None, meta_data=None, instrument_identifier=None):
        """
        Body3 - a model defined in Swagger
        """

        self._links = None
        self._id = None
        self._object = None
        self._state = None
        self._bank_account = None
        self._card = None
        self._buyer_information = None
        self._bill_to = None
        self._processing_information = None
        self._merchant_information = None
        self._meta_data = None
        self._instrument_identifier = None

        if links is not None:
          self.links = links
        if id is not None:
          self.id = id
        if object is not None:
          self.object = object
        if state is not None:
          self.state = state
        if bank_account is not None:
          self.bank_account = bank_account
        if card is not None:
          self.card = card
        if buyer_information is not None:
          self.buyer_information = buyer_information
        if bill_to is not None:
          self.bill_to = bill_to
        if processing_information is not None:
          self.processing_information = processing_information
        if merchant_information is not None:
          self.merchant_information = merchant_information
        if meta_data is not None:
          self.meta_data = meta_data
        if instrument_identifier is not None:
          self.instrument_identifier = instrument_identifier

    @property
    def links(self):
        """
        Gets the links of this Body3.

        :return: The links of this Body3.
        :rtype: Tmsv1instrumentidentifiersLinks
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this Body3.

        :param links: The links of this Body3.
        :type: Tmsv1instrumentidentifiersLinks
        """

        self._links = links

    @property
    def id(self):
        """
        Gets the id of this Body3.
        Unique identification number assigned by CyberSource to the submitted request.

        :return: The id of this Body3.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Body3.
        Unique identification number assigned by CyberSource to the submitted request.

        :param id: The id of this Body3.
        :type: str
        """

        self._id = id

    @property
    def object(self):
        """
        Gets the object of this Body3.
        Describes type of token. For example: customer, paymentInstrument or instrumentIdentifier.

        :return: The object of this Body3.
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """
        Sets the object of this Body3.
        Describes type of token. For example: customer, paymentInstrument or instrumentIdentifier.

        :param object: The object of this Body3.
        :type: str
        """
        allowed_values = ["paymentInstrument"]
        if object not in allowed_values:
            raise ValueError(
                "Invalid value for `object` ({0}), must be one of {1}"
                .format(object, allowed_values)
            )

        self._object = object

    @property
    def state(self):
        """
        Gets the state of this Body3.
        Current state of the token.

        :return: The state of this Body3.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Body3.
        Current state of the token.

        :param state: The state of this Body3.
        :type: str
        """
        allowed_values = ["ACTIVE", "CLOSED"]
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def bank_account(self):
        """
        Gets the bank_account of this Body3.

        :return: The bank_account of this Body3.
        :rtype: Tmsv1paymentinstrumentsBankAccount
        """
        return self._bank_account

    @bank_account.setter
    def bank_account(self, bank_account):
        """
        Sets the bank_account of this Body3.

        :param bank_account: The bank_account of this Body3.
        :type: Tmsv1paymentinstrumentsBankAccount
        """

        self._bank_account = bank_account

    @property
    def card(self):
        """
        Gets the card of this Body3.

        :return: The card of this Body3.
        :rtype: Tmsv1paymentinstrumentsCard
        """
        return self._card

    @card.setter
    def card(self, card):
        """
        Sets the card of this Body3.

        :param card: The card of this Body3.
        :type: Tmsv1paymentinstrumentsCard
        """

        self._card = card

    @property
    def buyer_information(self):
        """
        Gets the buyer_information of this Body3.

        :return: The buyer_information of this Body3.
        :rtype: Tmsv1paymentinstrumentsBuyerInformation
        """
        return self._buyer_information

    @buyer_information.setter
    def buyer_information(self, buyer_information):
        """
        Sets the buyer_information of this Body3.

        :param buyer_information: The buyer_information of this Body3.
        :type: Tmsv1paymentinstrumentsBuyerInformation
        """

        self._buyer_information = buyer_information

    @property
    def bill_to(self):
        """
        Gets the bill_to of this Body3.

        :return: The bill_to of this Body3.
        :rtype: Tmsv1paymentinstrumentsBillTo
        """
        return self._bill_to

    @bill_to.setter
    def bill_to(self, bill_to):
        """
        Sets the bill_to of this Body3.

        :param bill_to: The bill_to of this Body3.
        :type: Tmsv1paymentinstrumentsBillTo
        """

        self._bill_to = bill_to

    @property
    def processing_information(self):
        """
        Gets the processing_information of this Body3.

        :return: The processing_information of this Body3.
        :rtype: Tmsv1paymentinstrumentsProcessingInformation
        """
        return self._processing_information

    @processing_information.setter
    def processing_information(self, processing_information):
        """
        Sets the processing_information of this Body3.

        :param processing_information: The processing_information of this Body3.
        :type: Tmsv1paymentinstrumentsProcessingInformation
        """

        self._processing_information = processing_information

    @property
    def merchant_information(self):
        """
        Gets the merchant_information of this Body3.

        :return: The merchant_information of this Body3.
        :rtype: Tmsv1paymentinstrumentsMerchantInformation
        """
        return self._merchant_information

    @merchant_information.setter
    def merchant_information(self, merchant_information):
        """
        Sets the merchant_information of this Body3.

        :param merchant_information: The merchant_information of this Body3.
        :type: Tmsv1paymentinstrumentsMerchantInformation
        """

        self._merchant_information = merchant_information

    @property
    def meta_data(self):
        """
        Gets the meta_data of this Body3.

        :return: The meta_data of this Body3.
        :rtype: Tmsv1instrumentidentifiersMetadata
        """
        return self._meta_data

    @meta_data.setter
    def meta_data(self, meta_data):
        """
        Sets the meta_data of this Body3.

        :param meta_data: The meta_data of this Body3.
        :type: Tmsv1instrumentidentifiersMetadata
        """

        self._meta_data = meta_data

    @property
    def instrument_identifier(self):
        """
        Gets the instrument_identifier of this Body3.

        :return: The instrument_identifier of this Body3.
        :rtype: Tmsv1paymentinstrumentsInstrumentIdentifier
        """
        return self._instrument_identifier

    @instrument_identifier.setter
    def instrument_identifier(self, instrument_identifier):
        """
        Sets the instrument_identifier of this Body3.

        :param instrument_identifier: The instrument_identifier of this Body3.
        :type: Tmsv1paymentinstrumentsInstrumentIdentifier
        """

        self._instrument_identifier = instrument_identifier

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
        if not isinstance(other, Body3):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
