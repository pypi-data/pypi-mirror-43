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


class JsonWebKey(object):
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
        'kty': 'str',
        'use': 'str',
        'kid': 'str',
        'n': 'str',
        'e': 'str'
    }

    attribute_map = {
        'kty': 'kty',
        'use': 'use',
        'kid': 'kid',
        'n': 'n',
        'e': 'e'
    }

    def __init__(self, kty=None, use=None, kid=None, n=None, e=None):
        """
        JsonWebKey - a model defined in Swagger
        """

        self._kty = None
        self._use = None
        self._kid = None
        self._n = None
        self._e = None

        if kty is not None:
          self.kty = kty
        if use is not None:
          self.use = use
        if kid is not None:
          self.kid = kid
        if n is not None:
          self.n = n
        if e is not None:
          self.e = e

    @property
    def kty(self):
        """
        Gets the kty of this JsonWebKey.
        Algorithm used to encrypt the public key.

        :return: The kty of this JsonWebKey.
        :rtype: str
        """
        return self._kty

    @kty.setter
    def kty(self, kty):
        """
        Sets the kty of this JsonWebKey.
        Algorithm used to encrypt the public key.

        :param kty: The kty of this JsonWebKey.
        :type: str
        """

        self._kty = kty

    @property
    def use(self):
        """
        Gets the use of this JsonWebKey.
        Defines whether to use the key for encryption (enc) or verifying a signature (sig). Always returned as enc.

        :return: The use of this JsonWebKey.
        :rtype: str
        """
        return self._use

    @use.setter
    def use(self, use):
        """
        Sets the use of this JsonWebKey.
        Defines whether to use the key for encryption (enc) or verifying a signature (sig). Always returned as enc.

        :param use: The use of this JsonWebKey.
        :type: str
        """

        self._use = use

    @property
    def kid(self):
        """
        Gets the kid of this JsonWebKey.
        The key ID in JWK format.

        :return: The kid of this JsonWebKey.
        :rtype: str
        """
        return self._kid

    @kid.setter
    def kid(self, kid):
        """
        Sets the kid of this JsonWebKey.
        The key ID in JWK format.

        :param kid: The kid of this JsonWebKey.
        :type: str
        """

        self._kid = kid

    @property
    def n(self):
        """
        Gets the n of this JsonWebKey.
        JWK RSA Modulus

        :return: The n of this JsonWebKey.
        :rtype: str
        """
        return self._n

    @n.setter
    def n(self, n):
        """
        Sets the n of this JsonWebKey.
        JWK RSA Modulus

        :param n: The n of this JsonWebKey.
        :type: str
        """

        self._n = n

    @property
    def e(self):
        """
        Gets the e of this JsonWebKey.
        JWK RSA Exponent

        :return: The e of this JsonWebKey.
        :rtype: str
        """
        return self._e

    @e.setter
    def e(self, e):
        """
        Sets the e of this JsonWebKey.
        JWK RSA Exponent

        :param e: The e of this JsonWebKey.
        :type: str
        """

        self._e = e

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
        if not isinstance(other, JsonWebKey):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
