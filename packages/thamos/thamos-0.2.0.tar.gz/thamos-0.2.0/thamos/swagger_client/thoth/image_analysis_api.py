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


class ImageAnalysisApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_analyze(self, analysis_id, **kwargs):  # noqa: E501
        """Retrieve an analyzer result.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: Id of analysis that results should be retrieved. (required)
        :return: AnalysisResultResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_analyze_with_http_info(analysis_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_analyze_with_http_info(analysis_id, **kwargs)  # noqa: E501
            return data

    def get_analyze_with_http_info(self, analysis_id, **kwargs):  # noqa: E501
        """Retrieve an analyzer result.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze_with_http_info(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: Id of analysis that results should be retrieved. (required)
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
                    " to method get_analyze" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'analysis_id' is set
        if ('analysis_id' not in params or
                params['analysis_id'] is None):
            raise ValueError("Missing the required parameter `analysis_id` when calling `get_analyze`")  # noqa: E501

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
            '/analyze/{analysis_id}', 'GET',
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

    def get_analyze_by_hash(self, image_hash, **kwargs):  # noqa: E501
        """Retrieve an analyzer result.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze_by_hash(image_hash, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str image_hash: Image hash for identifying image (including hash type, now supported only \"sha256\"). (required)
        :return: AnalysisResultResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_analyze_by_hash_with_http_info(image_hash, **kwargs)  # noqa: E501
        else:
            (data) = self.get_analyze_by_hash_with_http_info(image_hash, **kwargs)  # noqa: E501
            return data

    def get_analyze_by_hash_with_http_info(self, image_hash, **kwargs):  # noqa: E501
        """Retrieve an analyzer result.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze_by_hash_with_http_info(image_hash, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str image_hash: Image hash for identifying image (including hash type, now supported only \"sha256\"). (required)
        :return: AnalysisResultResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['image_hash']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_analyze_by_hash" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'image_hash' is set
        if ('image_hash' not in params or
                params['image_hash'] is None):
            raise ValueError("Missing the required parameter `image_hash` when calling `get_analyze_by_hash`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'image_hash' in params:
            path_params['image_hash'] = params['image_hash']  # noqa: E501

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
            '/analyze/by-hash/{image_hash}', 'GET',
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

    def get_analyze_log(self, analysis_id, **kwargs):  # noqa: E501
        """Show logs of an analysis.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze_log(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of requested analysis. (required)
        :return: AnalysisLogResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_analyze_log_with_http_info(analysis_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_analyze_log_with_http_info(analysis_id, **kwargs)  # noqa: E501
            return data

    def get_analyze_log_with_http_info(self, analysis_id, **kwargs):  # noqa: E501
        """Show logs of an analysis.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze_log_with_http_info(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of requested analysis. (required)
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
                    " to method get_analyze_log" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'analysis_id' is set
        if ('analysis_id' not in params or
                params['analysis_id'] is None):
            raise ValueError("Missing the required parameter `analysis_id` when calling `get_analyze_log`")  # noqa: E501

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
            '/analyze/{analysis_id}/log', 'GET',
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

    def get_analyze_status(self, analysis_id, **kwargs):  # noqa: E501
        """Show analysis status.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze_status(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of requested analysis. (required)
        :return: AnalysisStatusResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_analyze_status_with_http_info(analysis_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_analyze_status_with_http_info(analysis_id, **kwargs)  # noqa: E501
            return data

    def get_analyze_status_with_http_info(self, analysis_id, **kwargs):  # noqa: E501
        """Show analysis status.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_analyze_status_with_http_info(analysis_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str analysis_id: An id of requested analysis. (required)
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
                    " to method get_analyze_status" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'analysis_id' is set
        if ('analysis_id' not in params or
                params['analysis_id'] is None):
            raise ValueError("Missing the required parameter `analysis_id` when calling `get_analyze_status`")  # noqa: E501

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
            '/analyze/{analysis_id}/status', 'GET',
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

    def list_analyze(self, **kwargs):  # noqa: E501
        """Retrieve a list of document ids for analyzer results.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_analyze(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: Page offset in pagination.
        :return: AnalysisListingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_analyze_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_analyze_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_analyze_with_http_info(self, **kwargs):  # noqa: E501
        """Retrieve a list of document ids for analyzer results.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_analyze_with_http_info(async_req=True)
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
                    " to method list_analyze" % key
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
            '/analyze', 'GET',
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

    def post_analyze(self, image, **kwargs):  # noqa: E501
        """Analyze the given image asynchronously.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_analyze(image, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str image: Name of image - can also specify remote registry to pull image from.  (required)
        :param str registry_user: Registry user to be used for pulling images from registry. 
        :param str registry_password: Registry password or token to be used for pulling images from registry. 
        :param bool debug: Run the given analyzer in a verbose mode so developers can debug analyzer. 
        :param bool verify_tls: Verify TLS certificates of registry from where images are pulled from. 
        :param bool force: Do not use cached results, always run analysis. 
        :return: AnalysisResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.post_analyze_with_http_info(image, **kwargs)  # noqa: E501
        else:
            (data) = self.post_analyze_with_http_info(image, **kwargs)  # noqa: E501
            return data

    def post_analyze_with_http_info(self, image, **kwargs):  # noqa: E501
        """Analyze the given image asynchronously.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_analyze_with_http_info(image, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str image: Name of image - can also specify remote registry to pull image from.  (required)
        :param str registry_user: Registry user to be used for pulling images from registry. 
        :param str registry_password: Registry password or token to be used for pulling images from registry. 
        :param bool debug: Run the given analyzer in a verbose mode so developers can debug analyzer. 
        :param bool verify_tls: Verify TLS certificates of registry from where images are pulled from. 
        :param bool force: Do not use cached results, always run analysis. 
        :return: AnalysisResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['image', 'registry_user', 'registry_password', 'debug', 'verify_tls', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_analyze" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'image' is set
        if ('image' not in params or
                params['image'] is None):
            raise ValueError("Missing the required parameter `image` when calling `post_analyze`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'image' in params:
            query_params.append(('image', params['image']))  # noqa: E501
        if 'registry_user' in params:
            query_params.append(('registry_user', params['registry_user']))  # noqa: E501
        if 'registry_password' in params:
            query_params.append(('registry_password', params['registry_password']))  # noqa: E501
        if 'debug' in params:
            query_params.append(('debug', params['debug']))  # noqa: E501
        if 'verify_tls' in params:
            query_params.append(('verify_tls', params['verify_tls']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

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
            '/analyze', 'POST',
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

    def post_image_metadata(self, image, **kwargs):  # noqa: E501
        """Get metadata for the given image  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_image_metadata(image, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str image: Name of image - can also specify remote registry to pull image from.  (required)
        :param str registry_user: Registry user to be used for pulling images from registry. 
        :param str registry_password: Registry password or token to be used for pulling images from registry. 
        :param bool verify_tls: Verify TLS certificates of registry from where images are pulled from. 
        :return: ImageMetadataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.post_image_metadata_with_http_info(image, **kwargs)  # noqa: E501
        else:
            (data) = self.post_image_metadata_with_http_info(image, **kwargs)  # noqa: E501
            return data

    def post_image_metadata_with_http_info(self, image, **kwargs):  # noqa: E501
        """Get metadata for the given image  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_image_metadata_with_http_info(image, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str image: Name of image - can also specify remote registry to pull image from.  (required)
        :param str registry_user: Registry user to be used for pulling images from registry. 
        :param str registry_password: Registry password or token to be used for pulling images from registry. 
        :param bool verify_tls: Verify TLS certificates of registry from where images are pulled from. 
        :return: ImageMetadataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['image', 'registry_user', 'registry_password', 'verify_tls']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_image_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'image' is set
        if ('image' not in params or
                params['image'] is None):
            raise ValueError("Missing the required parameter `image` when calling `post_image_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'image' in params:
            query_params.append(('image', params['image']))  # noqa: E501
        if 'registry_user' in params:
            query_params.append(('registry_user', params['registry_user']))  # noqa: E501
        if 'registry_password' in params:
            query_params.append(('registry_password', params['registry_password']))  # noqa: E501
        if 'verify_tls' in params:
            query_params.append(('verify_tls', params['verify_tls']))  # noqa: E501

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
            '/image/metadata', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ImageMetadataResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
