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


class AnalysisResponse(object):
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
        'analysis_id': 'str',
        'parameters': 'object',
        'cached': 'bool'
    }

    attribute_map = {
        'analysis_id': 'analysis_id',
        'parameters': 'parameters',
        'cached': 'cached'
    }

    def __init__(self, analysis_id=None, parameters=None, cached=None):  # noqa: E501
        """AnalysisResponse - a model defined in Swagger"""  # noqa: E501

        self._analysis_id = None
        self._parameters = None
        self._cached = None
        self.discriminator = None

        self.analysis_id = analysis_id
        self.parameters = parameters
        self.cached = cached

    @property
    def analysis_id(self):
        """Gets the analysis_id of this AnalysisResponse.  # noqa: E501

        An id of submitted analysis for checking its status and its results.   # noqa: E501

        :return: The analysis_id of this AnalysisResponse.  # noqa: E501
        :rtype: str
        """
        return self._analysis_id

    @analysis_id.setter
    def analysis_id(self, analysis_id):
        """Sets the analysis_id of this AnalysisResponse.

        An id of submitted analysis for checking its status and its results.   # noqa: E501

        :param analysis_id: The analysis_id of this AnalysisResponse.  # noqa: E501
        :type: str
        """
        if analysis_id is None:
            raise ValueError("Invalid value for `analysis_id`, must not be `None`")  # noqa: E501

        self._analysis_id = analysis_id

    @property
    def parameters(self):
        """Gets the parameters of this AnalysisResponse.  # noqa: E501

        Parameters echoed back to user (with default parameters if omitted).   # noqa: E501

        :return: The parameters of this AnalysisResponse.  # noqa: E501
        :rtype: object
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this AnalysisResponse.

        Parameters echoed back to user (with default parameters if omitted).   # noqa: E501

        :param parameters: The parameters of this AnalysisResponse.  # noqa: E501
        :type: object
        """
        if parameters is None:
            raise ValueError("Invalid value for `parameters`, must not be `None`")  # noqa: E501

        self._parameters = parameters

    @property
    def cached(self):
        """Gets the cached of this AnalysisResponse.  # noqa: E501

        If set to true the given analysis was picked from cache.   # noqa: E501

        :return: The cached of this AnalysisResponse.  # noqa: E501
        :rtype: bool
        """
        return self._cached

    @cached.setter
    def cached(self, cached):
        """Sets the cached of this AnalysisResponse.

        If set to true the given analysis was picked from cache.   # noqa: E501

        :param cached: The cached of this AnalysisResponse.  # noqa: E501
        :type: bool
        """
        if cached is None:
            raise ValueError("Invalid value for `cached`, must not be `None`")  # noqa: E501

        self._cached = cached

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
        if issubclass(AnalysisResponse, dict):
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
        if not isinstance(other, AnalysisResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
