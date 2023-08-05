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


class ReportingV3ReportDefinitionsNameGet200Response(object):
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
        'type': 'str',
        'report_definition_id': 'int',
        'report_defintion_name': 'str',
        'attributes': 'list[ReportingV3ReportDefinitionsNameGet200ResponseAttributes]',
        'supported_formats': 'list[str]',
        'description': 'str'
    }

    attribute_map = {
        'type': 'type',
        'report_definition_id': 'reportDefinitionId',
        'report_defintion_name': 'reportDefintionName',
        'attributes': 'attributes',
        'supported_formats': 'supportedFormats',
        'description': 'description'
    }

    def __init__(self, type=None, report_definition_id=None, report_defintion_name=None, attributes=None, supported_formats=None, description=None):
        """
        ReportingV3ReportDefinitionsNameGet200Response - a model defined in Swagger
        """

        self._type = None
        self._report_definition_id = None
        self._report_defintion_name = None
        self._attributes = None
        self._supported_formats = None
        self._description = None

        if type is not None:
          self.type = type
        if report_definition_id is not None:
          self.report_definition_id = report_definition_id
        if report_defintion_name is not None:
          self.report_defintion_name = report_defintion_name
        if attributes is not None:
          self.attributes = attributes
        if supported_formats is not None:
          self.supported_formats = supported_formats
        if description is not None:
          self.description = description

    @property
    def type(self):
        """
        Gets the type of this ReportingV3ReportDefinitionsNameGet200Response.

        :return: The type of this ReportingV3ReportDefinitionsNameGet200Response.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ReportingV3ReportDefinitionsNameGet200Response.

        :param type: The type of this ReportingV3ReportDefinitionsNameGet200Response.
        :type: str
        """

        self._type = type

    @property
    def report_definition_id(self):
        """
        Gets the report_definition_id of this ReportingV3ReportDefinitionsNameGet200Response.

        :return: The report_definition_id of this ReportingV3ReportDefinitionsNameGet200Response.
        :rtype: int
        """
        return self._report_definition_id

    @report_definition_id.setter
    def report_definition_id(self, report_definition_id):
        """
        Sets the report_definition_id of this ReportingV3ReportDefinitionsNameGet200Response.

        :param report_definition_id: The report_definition_id of this ReportingV3ReportDefinitionsNameGet200Response.
        :type: int
        """

        self._report_definition_id = report_definition_id

    @property
    def report_defintion_name(self):
        """
        Gets the report_defintion_name of this ReportingV3ReportDefinitionsNameGet200Response.

        :return: The report_defintion_name of this ReportingV3ReportDefinitionsNameGet200Response.
        :rtype: str
        """
        return self._report_defintion_name

    @report_defintion_name.setter
    def report_defintion_name(self, report_defintion_name):
        """
        Sets the report_defintion_name of this ReportingV3ReportDefinitionsNameGet200Response.

        :param report_defintion_name: The report_defintion_name of this ReportingV3ReportDefinitionsNameGet200Response.
        :type: str
        """

        self._report_defintion_name = report_defintion_name

    @property
    def attributes(self):
        """
        Gets the attributes of this ReportingV3ReportDefinitionsNameGet200Response.

        :return: The attributes of this ReportingV3ReportDefinitionsNameGet200Response.
        :rtype: list[ReportingV3ReportDefinitionsNameGet200ResponseAttributes]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this ReportingV3ReportDefinitionsNameGet200Response.

        :param attributes: The attributes of this ReportingV3ReportDefinitionsNameGet200Response.
        :type: list[ReportingV3ReportDefinitionsNameGet200ResponseAttributes]
        """

        self._attributes = attributes

    @property
    def supported_formats(self):
        """
        Gets the supported_formats of this ReportingV3ReportDefinitionsNameGet200Response.

        :return: The supported_formats of this ReportingV3ReportDefinitionsNameGet200Response.
        :rtype: list[str]
        """
        return self._supported_formats

    @supported_formats.setter
    def supported_formats(self, supported_formats):
        """
        Sets the supported_formats of this ReportingV3ReportDefinitionsNameGet200Response.

        :param supported_formats: The supported_formats of this ReportingV3ReportDefinitionsNameGet200Response.
        :type: list[str]
        """
        allowed_values = ["application/xml", "text/csv"]
        if not set(supported_formats).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `supported_formats` [{0}], must be a subset of [{1}]"
                .format(", ".join(map(str, set(supported_formats)-set(allowed_values))),
                        ", ".join(map(str, allowed_values)))
            )

        self._supported_formats = supported_formats

    @property
    def description(self):
        """
        Gets the description of this ReportingV3ReportDefinitionsNameGet200Response.

        :return: The description of this ReportingV3ReportDefinitionsNameGet200Response.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ReportingV3ReportDefinitionsNameGet200Response.

        :param description: The description of this ReportingV3ReportDefinitionsNameGet200Response.
        :type: str
        """

        self._description = description

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
        if not isinstance(other, ReportingV3ReportDefinitionsNameGet200Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
