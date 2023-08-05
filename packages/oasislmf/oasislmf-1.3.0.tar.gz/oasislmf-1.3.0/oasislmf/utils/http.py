# -*- coding: utf-8 -*-

# HTTP request/response MIME types and character set encoding type constants
MIME_TYPE_CSV = 'text/csv'
MIME_TYPE_JSON = 'application/json'
CHARSET_ENCODING_UTF8 = 'charset=utf-8'

# HTTP response status codes
HTTP_RESPONSE_OK = 200
HTTP_RESPONSE_BAD_REQUEST = 400
HTTP_RESPONSE_RESOURCE_NOT_FOUND = 404
HTTP_RESPONSE_INTERNAL_SERVER_ERROR = 500

# HTTP request content types
HTTP_REQUEST_CONTENT_TYPE_CSV = '; '.join([MIME_TYPE_CSV, CHARSET_ENCODING_UTF8])
HTTP_REQUEST_CONTENT_TYPE_JSON = '; '.join([MIME_TYPE_JSON, CHARSET_ENCODING_UTF8])
