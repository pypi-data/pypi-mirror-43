# coding: utf-8

"""
    Thoth user API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class LogMetadataAnnotations(object):
    """NOTE: This class is auto generated by the swagger code generator program.

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
        'buildlog_thoth_station_ninjacorresponding_build_configuration': 'str'
    }

    attribute_map = {
        'buildlog_thoth_station_ninjacorresponding_build_configuration': 'buildlog.thoth-station.ninja/corresponding-build-configuration'
    }

    def __init__(self, buildlog_thoth_station_ninjacorresponding_build_configuration=None):  # noqa: E501
        """LogMetadataAnnotations - a model defined in Swagger"""  # noqa: E501

        self._buildlog_thoth_station_ninjacorresponding_build_configuration = None
        self.discriminator = None

        if buildlog_thoth_station_ninjacorresponding_build_configuration is not None:
            self.buildlog_thoth_station_ninjacorresponding_build_configuration = buildlog_thoth_station_ninjacorresponding_build_configuration

    @property
    def buildlog_thoth_station_ninjacorresponding_build_configuration(self):
        """Gets the buildlog_thoth_station_ninjacorresponding_build_configuration of this LogMetadataAnnotations.  # noqa: E501

        Contains all particulars about the build log.   # noqa: E501

        :return: The buildlog_thoth_station_ninjacorresponding_build_configuration of this LogMetadataAnnotations.  # noqa: E501
        :rtype: str
        """
        return self._buildlog_thoth_station_ninjacorresponding_build_configuration

    @buildlog_thoth_station_ninjacorresponding_build_configuration.setter
    def buildlog_thoth_station_ninjacorresponding_build_configuration(self, buildlog_thoth_station_ninjacorresponding_build_configuration):
        """Sets the buildlog_thoth_station_ninjacorresponding_build_configuration of this LogMetadataAnnotations.

        Contains all particulars about the build log.   # noqa: E501

        :param buildlog_thoth_station_ninjacorresponding_build_configuration: The buildlog_thoth_station_ninjacorresponding_build_configuration of this LogMetadataAnnotations.  # noqa: E501
        :type: str
        """

        self._buildlog_thoth_station_ninjacorresponding_build_configuration = buildlog_thoth_station_ninjacorresponding_build_configuration

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(LogMetadataAnnotations, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, LogMetadataAnnotations):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
