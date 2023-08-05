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


class Ptsv2paymentsidcapturesMerchantInformation(object):
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
        'merchant_descriptor': 'Ptsv2paymentsMerchantInformationMerchantDescriptor',
        'card_acceptor_reference_number': 'str',
        'category_code': 'int',
        'vat_registration_number': 'str',
        'service_fee_descriptor': 'Ptsv2paymentsMerchantInformationServiceFeeDescriptor',
        'tax_id': 'str'
    }

    attribute_map = {
        'merchant_descriptor': 'merchantDescriptor',
        'card_acceptor_reference_number': 'cardAcceptorReferenceNumber',
        'category_code': 'categoryCode',
        'vat_registration_number': 'vatRegistrationNumber',
        'service_fee_descriptor': 'serviceFeeDescriptor',
        'tax_id': 'taxId'
    }

    def __init__(self, merchant_descriptor=None, card_acceptor_reference_number=None, category_code=None, vat_registration_number=None, service_fee_descriptor=None, tax_id=None):
        """
        Ptsv2paymentsidcapturesMerchantInformation - a model defined in Swagger
        """

        self._merchant_descriptor = None
        self._card_acceptor_reference_number = None
        self._category_code = None
        self._vat_registration_number = None
        self._service_fee_descriptor = None
        self._tax_id = None

        if merchant_descriptor is not None:
          self.merchant_descriptor = merchant_descriptor
        if card_acceptor_reference_number is not None:
          self.card_acceptor_reference_number = card_acceptor_reference_number
        if category_code is not None:
          self.category_code = category_code
        if vat_registration_number is not None:
          self.vat_registration_number = vat_registration_number
        if service_fee_descriptor is not None:
          self.service_fee_descriptor = service_fee_descriptor
        if tax_id is not None:
          self.tax_id = tax_id

    @property
    def merchant_descriptor(self):
        """
        Gets the merchant_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.

        :return: The merchant_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.
        :rtype: Ptsv2paymentsMerchantInformationMerchantDescriptor
        """
        return self._merchant_descriptor

    @merchant_descriptor.setter
    def merchant_descriptor(self, merchant_descriptor):
        """
        Sets the merchant_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.

        :param merchant_descriptor: The merchant_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.
        :type: Ptsv2paymentsMerchantInformationMerchantDescriptor
        """

        self._merchant_descriptor = merchant_descriptor

    @property
    def card_acceptor_reference_number(self):
        """
        Gets the card_acceptor_reference_number of this Ptsv2paymentsidcapturesMerchantInformation.
        Reference number that facilitates card acceptor/corporation communication and record keeping.  For processor-specific information, see the card_acceptor_ref_number field in [Level II and Level III Processing Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/Level_2_3_SCMP_API/html) 

        :return: The card_acceptor_reference_number of this Ptsv2paymentsidcapturesMerchantInformation.
        :rtype: str
        """
        return self._card_acceptor_reference_number

    @card_acceptor_reference_number.setter
    def card_acceptor_reference_number(self, card_acceptor_reference_number):
        """
        Sets the card_acceptor_reference_number of this Ptsv2paymentsidcapturesMerchantInformation.
        Reference number that facilitates card acceptor/corporation communication and record keeping.  For processor-specific information, see the card_acceptor_ref_number field in [Level II and Level III Processing Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/Level_2_3_SCMP_API/html) 

        :param card_acceptor_reference_number: The card_acceptor_reference_number of this Ptsv2paymentsidcapturesMerchantInformation.
        :type: str
        """
        if card_acceptor_reference_number is not None and len(card_acceptor_reference_number) > 25:
            raise ValueError("Invalid value for `card_acceptor_reference_number`, length must be less than or equal to `25`")

        self._card_acceptor_reference_number = card_acceptor_reference_number

    @property
    def category_code(self):
        """
        Gets the category_code of this Ptsv2paymentsidcapturesMerchantInformation.
        Four-digit number that the payment card industry uses to classify merchants into market segments. Visa assigned one or more of these values to your business when you started accepting Visa cards.  If you do not include this field in your request, CyberSource uses the value in your CyberSource account.  For processor-specific information, see the merchant_category_code field in [Credit Card Services Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html)  See \"Aggregator Support,\" page 100.  **CyberSource through VisaNet**\\ The value for this field corresponds to the following data in the TC 33 capture file5: - Record: CP01 TCR4 - Position: 150-153 - Field: Merchant Category Code 

        :return: The category_code of this Ptsv2paymentsidcapturesMerchantInformation.
        :rtype: int
        """
        return self._category_code

    @category_code.setter
    def category_code(self, category_code):
        """
        Sets the category_code of this Ptsv2paymentsidcapturesMerchantInformation.
        Four-digit number that the payment card industry uses to classify merchants into market segments. Visa assigned one or more of these values to your business when you started accepting Visa cards.  If you do not include this field in your request, CyberSource uses the value in your CyberSource account.  For processor-specific information, see the merchant_category_code field in [Credit Card Services Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html)  See \"Aggregator Support,\" page 100.  **CyberSource through VisaNet**\\ The value for this field corresponds to the following data in the TC 33 capture file5: - Record: CP01 TCR4 - Position: 150-153 - Field: Merchant Category Code 

        :param category_code: The category_code of this Ptsv2paymentsidcapturesMerchantInformation.
        :type: int
        """
        if category_code is not None and category_code > 9999:
            raise ValueError("Invalid value for `category_code`, must be a value less than or equal to `9999`")

        self._category_code = category_code

    @property
    def vat_registration_number(self):
        """
        Gets the vat_registration_number of this Ptsv2paymentsidcapturesMerchantInformation.
        Your government-assigned tax identification number.  For CtV processors, the maximum length is 20.  For other processor-specific information, see the merchant_vat_registration_number field in [Level II and Level III Processing Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/Level_2_3_SCMP_API/html) 

        :return: The vat_registration_number of this Ptsv2paymentsidcapturesMerchantInformation.
        :rtype: str
        """
        return self._vat_registration_number

    @vat_registration_number.setter
    def vat_registration_number(self, vat_registration_number):
        """
        Sets the vat_registration_number of this Ptsv2paymentsidcapturesMerchantInformation.
        Your government-assigned tax identification number.  For CtV processors, the maximum length is 20.  For other processor-specific information, see the merchant_vat_registration_number field in [Level II and Level III Processing Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/Level_2_3_SCMP_API/html) 

        :param vat_registration_number: The vat_registration_number of this Ptsv2paymentsidcapturesMerchantInformation.
        :type: str
        """
        if vat_registration_number is not None and len(vat_registration_number) > 21:
            raise ValueError("Invalid value for `vat_registration_number`, length must be less than or equal to `21`")

        self._vat_registration_number = vat_registration_number

    @property
    def service_fee_descriptor(self):
        """
        Gets the service_fee_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.

        :return: The service_fee_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.
        :rtype: Ptsv2paymentsMerchantInformationServiceFeeDescriptor
        """
        return self._service_fee_descriptor

    @service_fee_descriptor.setter
    def service_fee_descriptor(self, service_fee_descriptor):
        """
        Sets the service_fee_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.

        :param service_fee_descriptor: The service_fee_descriptor of this Ptsv2paymentsidcapturesMerchantInformation.
        :type: Ptsv2paymentsMerchantInformationServiceFeeDescriptor
        """

        self._service_fee_descriptor = service_fee_descriptor

    @property
    def tax_id(self):
        """
        Gets the tax_id of this Ptsv2paymentsidcapturesMerchantInformation.
        Your Cadastro Nacional da Pessoa Jurídica (CNPJ) number.  This field is supported only for BNDES transactions on CyberSource through VisaNet. See BNDES.  The value for this field corresponds to the following data in the TC 33 capture file5: - Record: CP07 TCR6 - Position: 40-59 - Field: BNDES Reference Field 1 

        :return: The tax_id of this Ptsv2paymentsidcapturesMerchantInformation.
        :rtype: str
        """
        return self._tax_id

    @tax_id.setter
    def tax_id(self, tax_id):
        """
        Sets the tax_id of this Ptsv2paymentsidcapturesMerchantInformation.
        Your Cadastro Nacional da Pessoa Jurídica (CNPJ) number.  This field is supported only for BNDES transactions on CyberSource through VisaNet. See BNDES.  The value for this field corresponds to the following data in the TC 33 capture file5: - Record: CP07 TCR6 - Position: 40-59 - Field: BNDES Reference Field 1 

        :param tax_id: The tax_id of this Ptsv2paymentsidcapturesMerchantInformation.
        :type: str
        """
        if tax_id is not None and len(tax_id) > 15:
            raise ValueError("Invalid value for `tax_id`, length must be less than or equal to `15`")

        self._tax_id = tax_id

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
        if not isinstance(other, Ptsv2paymentsidcapturesMerchantInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
