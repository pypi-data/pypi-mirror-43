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


class Ptsv2creditsProcessingInformationBankTransferOptions(object):
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
        'customer_memo': 'str',
        'sec_code': 'str',
        'terminal_city': 'str',
        'terminal_state': 'str',
        'effective_date': 'str',
        'partial_payment_id': 'str',
        'settlement_method': 'str'
    }

    attribute_map = {
        'customer_memo': 'customerMemo',
        'sec_code': 'secCode',
        'terminal_city': 'terminalCity',
        'terminal_state': 'terminalState',
        'effective_date': 'effectiveDate',
        'partial_payment_id': 'partialPaymentId',
        'settlement_method': 'settlementMethod'
    }

    def __init__(self, customer_memo=None, sec_code=None, terminal_city=None, terminal_state=None, effective_date=None, partial_payment_id=None, settlement_method=None):
        """
        Ptsv2creditsProcessingInformationBankTransferOptions - a model defined in Swagger
        """

        self._customer_memo = None
        self._sec_code = None
        self._terminal_city = None
        self._terminal_state = None
        self._effective_date = None
        self._partial_payment_id = None
        self._settlement_method = None

        if customer_memo is not None:
          self.customer_memo = customer_memo
        if sec_code is not None:
          self.sec_code = sec_code
        if terminal_city is not None:
          self.terminal_city = terminal_city
        if terminal_state is not None:
          self.terminal_state = terminal_state
        if effective_date is not None:
          self.effective_date = effective_date
        if partial_payment_id is not None:
          self.partial_payment_id = partial_payment_id
        if settlement_method is not None:
          self.settlement_method = settlement_method

    @property
    def customer_memo(self):
        """
        Gets the customer_memo of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Payment related information.  This information is included on the customer’s statement. 

        :return: The customer_memo of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._customer_memo

    @customer_memo.setter
    def customer_memo(self, customer_memo):
        """
        Sets the customer_memo of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Payment related information.  This information is included on the customer’s statement. 

        :param customer_memo: The customer_memo of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :type: str
        """
        if customer_memo is not None and len(customer_memo) > 80:
            raise ValueError("Invalid value for `customer_memo`, length must be less than or equal to `80`")

        self._customer_memo = customer_memo

    @property
    def sec_code(self):
        """
        Gets the sec_code of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Authorization method used for the transaction. See \"SEC Codes,\" page 89.  TeleCheck Accepts only the following values: - **PPD** - **TEL** - **WEB** 

        :return: The sec_code of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._sec_code

    @sec_code.setter
    def sec_code(self, sec_code):
        """
        Sets the sec_code of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Authorization method used for the transaction. See \"SEC Codes,\" page 89.  TeleCheck Accepts only the following values: - **PPD** - **TEL** - **WEB** 

        :param sec_code: The sec_code of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :type: str
        """
        if sec_code is not None and len(sec_code) > 3:
            raise ValueError("Invalid value for `sec_code`, length must be less than or equal to `3`")

        self._sec_code = sec_code

    @property
    def terminal_city(self):
        """
        Gets the terminal_city of this Ptsv2creditsProcessingInformationBankTransferOptions.
        City in which the terminal is located. If more than four alphanumeric characters are submitted, the transaction will be declined.  You cannot include any special characters. 

        :return: The terminal_city of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._terminal_city

    @terminal_city.setter
    def terminal_city(self, terminal_city):
        """
        Sets the terminal_city of this Ptsv2creditsProcessingInformationBankTransferOptions.
        City in which the terminal is located. If more than four alphanumeric characters are submitted, the transaction will be declined.  You cannot include any special characters. 

        :param terminal_city: The terminal_city of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :type: str
        """
        if terminal_city is not None and len(terminal_city) > 4:
            raise ValueError("Invalid value for `terminal_city`, length must be less than or equal to `4`")

        self._terminal_city = terminal_city

    @property
    def terminal_state(self):
        """
        Gets the terminal_state of this Ptsv2creditsProcessingInformationBankTransferOptions.
        State in which the terminal is located. If more than two alphanumeric characters are submitted, the transaction will be declined.  You cannot include any special characters. 

        :return: The terminal_state of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._terminal_state

    @terminal_state.setter
    def terminal_state(self, terminal_state):
        """
        Sets the terminal_state of this Ptsv2creditsProcessingInformationBankTransferOptions.
        State in which the terminal is located. If more than two alphanumeric characters are submitted, the transaction will be declined.  You cannot include any special characters. 

        :param terminal_state: The terminal_state of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :type: str
        """
        if terminal_state is not None and len(terminal_state) > 2:
            raise ValueError("Invalid value for `terminal_state`, length must be less than or equal to `2`")

        self._terminal_state = terminal_state

    @property
    def effective_date(self):
        """
        Gets the effective_date of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Effective date for the transaction. The effective date must be within 45 days of the current day. If you do not include this value, CyberSource sets the effective date to the next business day.  Format: `MMDDYYYY`  Supported only for the CyberSource ACH Service. 

        :return: The effective_date of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._effective_date

    @effective_date.setter
    def effective_date(self, effective_date):
        """
        Sets the effective_date of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Effective date for the transaction. The effective date must be within 45 days of the current day. If you do not include this value, CyberSource sets the effective date to the next business day.  Format: `MMDDYYYY`  Supported only for the CyberSource ACH Service. 

        :param effective_date: The effective_date of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :type: str
        """
        if effective_date is not None and len(effective_date) > 8:
            raise ValueError("Invalid value for `effective_date`, length must be less than or equal to `8`")

        self._effective_date = effective_date

    @property
    def partial_payment_id(self):
        """
        Gets the partial_payment_id of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Identifier for a partial payment or partial credit.  The value for each debit request or credit request must be unique within the scope of the order. See \"Multiple Partial Credits,\" page 41. 

        :return: The partial_payment_id of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._partial_payment_id

    @partial_payment_id.setter
    def partial_payment_id(self, partial_payment_id):
        """
        Sets the partial_payment_id of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Identifier for a partial payment or partial credit.  The value for each debit request or credit request must be unique within the scope of the order. See \"Multiple Partial Credits,\" page 41. 

        :param partial_payment_id: The partial_payment_id of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :type: str
        """
        if partial_payment_id is not None and len(partial_payment_id) > 25:
            raise ValueError("Invalid value for `partial_payment_id`, length must be less than or equal to `25`")

        self._partial_payment_id = partial_payment_id

    @property
    def settlement_method(self):
        """
        Gets the settlement_method of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Method used for settlement.  Possible values: - **A**: Automated Clearing House (default for credits and for transactions using Canadian dollars) - **F**: Facsimile draft (U.S. dollars only) - **B**: Best possible (U.S. dollars only) (default if the field has not already been configured for your merchant ID)  See \"Settlement Delivery Methods,\" page 44. 

        :return: The settlement_method of this Ptsv2creditsProcessingInformationBankTransferOptions.
        :rtype: str
        """
        return self._settlement_method

    @settlement_method.setter
    def settlement_method(self, settlement_method):
        """
        Sets the settlement_method of this Ptsv2creditsProcessingInformationBankTransferOptions.
        Method used for settlement.  Possible values: - **A**: Automated Clearing House (default for credits and for transactions using Canadian dollars) - **F**: Facsimile draft (U.S. dollars only) - **B**: Best possible (U.S. dollars only) (default if the field has not already been configured for your merchant ID)  See \"Settlement Delivery Methods,\" page 44. 

        :param settlement_method: The settlement_method of this Ptsv2creditsProcessingInformationBankTransferOptions.
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
        if not isinstance(other, Ptsv2creditsProcessingInformationBankTransferOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
