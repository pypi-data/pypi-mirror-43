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


class ReportingV3ReportsGet200Response(object):
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
        'reports': 'list[ReportingV3ReportsGet200ResponseReports]'
    }

    attribute_map = {
        'reports': 'reports'
    }

    def __init__(self, reports=None):
        """
        ReportingV3ReportsGet200Response - a model defined in Swagger
        """

        self._reports = None

        if reports is not None:
          self.reports = reports

    @property
    def reports(self):
        """
        Gets the reports of this ReportingV3ReportsGet200Response.

        :return: The reports of this ReportingV3ReportsGet200Response.
        :rtype: list[ReportingV3ReportsGet200ResponseReports]
        """
        return self._reports

    @reports.setter
    def reports(self, reports):
        """
        Sets the reports of this ReportingV3ReportsGet200Response.

        :param reports: The reports of this ReportingV3ReportsGet200Response.
        :type: list[ReportingV3ReportsGet200ResponseReports]
        """

        self._reports = reports

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
        if not isinstance(other, ReportingV3ReportsGet200Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
