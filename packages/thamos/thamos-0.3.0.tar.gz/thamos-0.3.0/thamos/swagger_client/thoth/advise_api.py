# coding: utf-8

"""
    Thoth user API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from thamos.swagger_client.api_client import ApiClient


class AdviseApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_advise_python(self, analysis_id, **kwargs):  # noqa: E501
        """Get computeted adviser result based on its id.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_advise_python(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: Advise id returned on advise request. (required)
        :return: AnalysisResultResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_advise_python_with_http_info(analysis_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_advise_python_with_http_info(analysis_id, **kwargs)  # noqa: E501
            return data

    def get_advise_python_with_http_info(self, analysis_id, **kwargs):  # noqa: E501
        """Get computeted adviser result based on its id.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_advise_python_with_http_info(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: Advise id returned on advise request. (required)
        :return: AnalysisResultResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['analysis_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_advise_python" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'analysis_id' is set
        if ('analysis_id' not in params or
                params['analysis_id'] is None):
            raise ValueError("Missing the required parameter `analysis_id` when calling `get_advise_python`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'analysis_id' in params:
            path_params['analysis_id'] = params['analysis_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/advise/python/{analysis_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnalysisResultResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_advise_python_log(self, analysis_id, **kwargs):  # noqa: E501
        """Retrieve a adviser run log.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_advise_python_log(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of analysis for which log should be retrieved. (required)
        :return: AnalysisLogResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_advise_python_log_with_http_info(analysis_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_advise_python_log_with_http_info(analysis_id, **kwargs)  # noqa: E501
            return data

    def get_advise_python_log_with_http_info(self, analysis_id, **kwargs):  # noqa: E501
        """Retrieve a adviser run log.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_advise_python_log_with_http_info(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of analysis for which log should be retrieved. (required)
        :return: AnalysisLogResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['analysis_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_advise_python_log" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'analysis_id' is set
        if ('analysis_id' not in params or
                params['analysis_id'] is None):
            raise ValueError("Missing the required parameter `analysis_id` when calling `get_advise_python_log`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'analysis_id' in params:
            path_params['analysis_id'] = params['analysis_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/advise/python/{analysis_id}/log', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnalysisLogResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_advise_python_status(self, analysis_id, **kwargs):  # noqa: E501
        """Show status of an adviser computing recomemendations.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_advise_python_status(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of requested adviser run. (required)
        :return: AnalysisStatusResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_advise_python_status_with_http_info(analysis_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_advise_python_status_with_http_info(analysis_id, **kwargs)  # noqa: E501
            return data

    def get_advise_python_status_with_http_info(self, analysis_id, **kwargs):  # noqa: E501
        """Show status of an adviser computing recomemendations.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_advise_python_status_with_http_info(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of requested adviser run. (required)
        :return: AnalysisStatusResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['analysis_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_advise_python_status" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'analysis_id' is set
        if ('analysis_id' not in params or
                params['analysis_id'] is None):
            raise ValueError("Missing the required parameter `analysis_id` when calling `get_advise_python_status`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'analysis_id' in params:
            path_params['analysis_id'] = params['analysis_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/advise/python/{analysis_id}/status', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnalysisStatusResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_advise_python(self, **kwargs):  # noqa: E501
        """Get adviser results available.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_advise_python(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: Page offset in pagination.
        :return: AnalysisListingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_advise_python_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_advise_python_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_advise_python_with_http_info(self, **kwargs):  # noqa: E501
        """Get adviser results available.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_advise_python_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: Page offset in pagination.
        :return: AnalysisListingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_advise_python" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/advise/python', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnalysisListingResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_advise_python(self, input, recommendation_type, **kwargs):  # noqa: E501
        """Get advise for Python ecosystem.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_advise_python(input, recommendation_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdviseInput input: Specification of Python application stack with runtime specific information. (required)
        :param str recommendation_type: Recommendation type. (required)
        :param int count: Number of software stacks that should be returned.
        :param int limit: Limit number of software stacks scored.
        :param bool debug: Run the given adviser in a verbose mode so developers can debug it. 
        :param bool force: Do not use cached results, always run adviser. 
        :return: AnalysisResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.post_advise_python_with_http_info(input, recommendation_type, **kwargs)  # noqa: E501
        else:
            (data) = self.post_advise_python_with_http_info(input, recommendation_type, **kwargs)  # noqa: E501
            return data

    def post_advise_python_with_http_info(self, input, recommendation_type, **kwargs):  # noqa: E501
        """Get advise for Python ecosystem.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_advise_python_with_http_info(input, recommendation_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AdviseInput input: Specification of Python application stack with runtime specific information. (required)
        :param str recommendation_type: Recommendation type. (required)
        :param int count: Number of software stacks that should be returned.
        :param int limit: Limit number of software stacks scored.
        :param bool debug: Run the given adviser in a verbose mode so developers can debug it. 
        :param bool force: Do not use cached results, always run adviser. 
        :return: AnalysisResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['input', 'recommendation_type', 'count', 'limit', 'debug', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_advise_python" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'input' is set
        if ('input' not in params or
                params['input'] is None):
            raise ValueError("Missing the required parameter `input` when calling `post_advise_python`")  # noqa: E501
        # verify the required parameter 'recommendation_type' is set
        if ('recommendation_type' not in params or
                params['recommendation_type'] is None):
            raise ValueError("Missing the required parameter `recommendation_type` when calling `post_advise_python`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'recommendation_type' in params:
            query_params.append(('recommendation_type', params['recommendation_type']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'debug' in params:
            query_params.append(('debug', params['debug']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'input' in params:
            body_params = params['input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/advise/python', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnalysisResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
