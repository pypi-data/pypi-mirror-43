# coding: utf-8

"""
    Wodby API Client

    Wodby Developer Documentation https://wodby.com/docs/dev  # noqa: E501

    OpenAPI spec version: 3.0.10
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class RequestAppCreateGit(object):
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
        'repo_id': 'str',
        'tree_ish': 'str'
    }

    attribute_map = {
        'repo_id': 'repo_id',
        'tree_ish': 'tree_ish'
    }

    def __init__(self, repo_id=None, tree_ish=None):  # noqa: E501
        """RequestAppCreateGit - a model defined in Swagger"""  # noqa: E501

        self._repo_id = None
        self._tree_ish = None
        self.discriminator = None

        self.repo_id = repo_id
        if tree_ish is not None:
            self.tree_ish = tree_ish

    @property
    def repo_id(self):
        """Gets the repo_id of this RequestAppCreateGit.  # noqa: E501


        :return: The repo_id of this RequestAppCreateGit.  # noqa: E501
        :rtype: str
        """
        return self._repo_id

    @repo_id.setter
    def repo_id(self, repo_id):
        """Sets the repo_id of this RequestAppCreateGit.


        :param repo_id: The repo_id of this RequestAppCreateGit.  # noqa: E501
        :type: str
        """
        if repo_id is None:
            raise ValueError("Invalid value for `repo_id`, must not be `None`")  # noqa: E501
        if repo_id is not None and not re.search('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', repo_id):  # noqa: E501
            raise ValueError("Invalid value for `repo_id`, must be a follow pattern or equal to `/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/`")  # noqa: E501

        self._repo_id = repo_id

    @property
    def tree_ish(self):
        """Gets the tree_ish of this RequestAppCreateGit.  # noqa: E501

        Commit, branch or tag  # noqa: E501

        :return: The tree_ish of this RequestAppCreateGit.  # noqa: E501
        :rtype: str
        """
        return self._tree_ish

    @tree_ish.setter
    def tree_ish(self, tree_ish):
        """Sets the tree_ish of this RequestAppCreateGit.

        Commit, branch or tag  # noqa: E501

        :param tree_ish: The tree_ish of this RequestAppCreateGit.  # noqa: E501
        :type: str
        """

        self._tree_ish = tree_ish

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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RequestAppCreateGit):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
