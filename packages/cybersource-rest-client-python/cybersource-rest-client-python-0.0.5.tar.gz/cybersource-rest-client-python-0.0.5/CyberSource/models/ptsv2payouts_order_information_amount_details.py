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


class Ptsv2payoutsOrderInformationAmountDetails(object):
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
        'total_amount': 'str',
        'currency': 'str',
        'surcharge': 'Ptsv2payoutsOrderInformationAmountDetailsSurcharge'
    }

    attribute_map = {
        'total_amount': 'totalAmount',
        'currency': 'currency',
        'surcharge': 'surcharge'
    }

    def __init__(self, total_amount=None, currency=None, surcharge=None):
        """
        Ptsv2payoutsOrderInformationAmountDetails - a model defined in Swagger
        """

        self._total_amount = None
        self._currency = None
        self._surcharge = None

        if total_amount is not None:
          self.total_amount = total_amount
        if currency is not None:
          self.currency = currency
        if surcharge is not None:
          self.surcharge = surcharge

    @property
    def total_amount(self):
        """
        Gets the total_amount of this Ptsv2payoutsOrderInformationAmountDetails.
        Grand total for the order. You can include a decimal point (.), but no other special characters. CyberSource truncates the amount to the correct number of decimal places.  * CTV, FDCCompass, Paymentech (<= 12)  For processor-specific information, see the grand_total_amount field in [Credit Card Services Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html) 

        :return: The total_amount of this Ptsv2payoutsOrderInformationAmountDetails.
        :rtype: str
        """
        return self._total_amount

    @total_amount.setter
    def total_amount(self, total_amount):
        """
        Sets the total_amount of this Ptsv2payoutsOrderInformationAmountDetails.
        Grand total for the order. You can include a decimal point (.), but no other special characters. CyberSource truncates the amount to the correct number of decimal places.  * CTV, FDCCompass, Paymentech (<= 12)  For processor-specific information, see the grand_total_amount field in [Credit Card Services Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html) 

        :param total_amount: The total_amount of this Ptsv2payoutsOrderInformationAmountDetails.
        :type: str
        """
        if total_amount is not None and len(total_amount) > 19:
            raise ValueError("Invalid value for `total_amount`, length must be less than or equal to `19`")

        self._total_amount = total_amount

    @property
    def currency(self):
        """
        Gets the currency of this Ptsv2payoutsOrderInformationAmountDetails.
        Currency used for the order. Use the three-character ISO Standard Currency Codes.  For an authorization reversal or a capture, you must use the same currency that you used in your request for Payment API. 

        :return: The currency of this Ptsv2payoutsOrderInformationAmountDetails.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """
        Sets the currency of this Ptsv2payoutsOrderInformationAmountDetails.
        Currency used for the order. Use the three-character ISO Standard Currency Codes.  For an authorization reversal or a capture, you must use the same currency that you used in your request for Payment API. 

        :param currency: The currency of this Ptsv2payoutsOrderInformationAmountDetails.
        :type: str
        """
        if currency is not None and len(currency) > 3:
            raise ValueError("Invalid value for `currency`, length must be less than or equal to `3`")

        self._currency = currency

    @property
    def surcharge(self):
        """
        Gets the surcharge of this Ptsv2payoutsOrderInformationAmountDetails.

        :return: The surcharge of this Ptsv2payoutsOrderInformationAmountDetails.
        :rtype: Ptsv2payoutsOrderInformationAmountDetailsSurcharge
        """
        return self._surcharge

    @surcharge.setter
    def surcharge(self, surcharge):
        """
        Sets the surcharge of this Ptsv2payoutsOrderInformationAmountDetails.

        :param surcharge: The surcharge of this Ptsv2payoutsOrderInformationAmountDetails.
        :type: Ptsv2payoutsOrderInformationAmountDetailsSurcharge
        """

        self._surcharge = surcharge

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
        if not isinstance(other, Ptsv2payoutsOrderInformationAmountDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
