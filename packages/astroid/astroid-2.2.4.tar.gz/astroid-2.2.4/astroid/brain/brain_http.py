# Copyright (c) 2018 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/PyCQA/astroid/blob/master/COPYING.LESSER

"""Astroid brain hints for some of the `http` module."""
import textwrap

import astroid
from astroid.builder import AstroidBuilder


def _http_transform():
    return AstroidBuilder(astroid.MANAGER).string_build(
        textwrap.dedent(
            """
    from http import HTTPStatus

    CONTINUE = HTTPStatus.CONTINUE
    SWITCHING_PROTOCOLS = HTTPStatus.SWITCHING_PROTOCOLS
    PROCESSING = HTTPStatus.PROCESSING
    OK = HTTPStatus.OK
    CREATED = HTTPStatus.CREATED
    ACCEPTED = HTTPStatus.ACCEPTED
    NON_AUTHORITATIVE_INFORMATION = HTTPStatus.NON_AUTHORITATIVE_INFORMATION
    NO_CONTENT = HTTPStatus.NO_CONTENT
    RESET_CONTENT = HTTPStatus.RESET_CONTENT
    PARTIAL_CONTENT = HTTPStatus.PARTIAL_CONTENT
    MULTI_STATUS = HTTPStatus.MULTI_STATUS
    ALREADY_REPORTED = HTTPStatus.ALREADY_REPORTED
    IM_USED = HTTPStatus.IM_USED
    MULTIPLE_CHOICES = HTTPStatus.MULTIPLE_CHOICES
    MOVED_PERMANENTLY = HTTPStatus.MOVED_PERMANENTLY
    FOUND = HTTPStatus.FOUND
    SEE_OTHER = HTTPStatus.SEE_OTHER
    NOT_MODIFIED = HTTPStatus.NOT_MODIFIED
    USE_PROXY = HTTPStatus.USE_PROXY
    TEMPORARY_REDIRECT = HTTPStatus.TEMPORARY_REDIRECT
    PERMANENT_REDIRECT = HTTPStatus.PERMANENT_REDIRECT
    BAD_REQUEST = HTTPStatus.BAD_REQUEST
    UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    PAYMENT_REQUIRED = HTTPStatus.PAYMENT_REQUIRED
    FORBIDDEN = HTTPStatus.FORBIDDEN
    NOT_FOUND = HTTPStatus.NOT_FOUND
    METHOD_NOT_ALLOWED = HTTPStatus.METHOD_NOT_ALLOWED
    NOT_ACCEPTABLE = HTTPStatus.NOT_ACCEPTABLE
    PROXY_AUTHENTICATION_REQUIRED = HTTPStatus.PROXY_AUTHENTICATION_REQUIRED
    REQUEST_TIMEOUT = HTTPStatus.REQUEST_TIMEOUT
    CONFLICT = HTTPStatus.CONFLICT
    GONE = HTTPStatus.GONE
    LENGTH_REQUIRED = HTTPStatus.LENGTH_REQUIRED
    PRECONDITION_FAILED = HTTPStatus.PRECONDITION_FAILED
    REQUEST_ENTITY_TOO_LARGE = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
    REQUEST_URI_TOO_LONG = HTTPStatus.REQUEST_URI_TOO_LONG
    UNSUPPORTED_MEDIA_TYPE = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    REQUESTED_RANGE_NOT_SATISFIABLE = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
    EXPECTATION_FAILED = HTTPStatus.EXPECTATION_FAILED
    UNPROCESSABLE_ENTITY = HTTPStatus.UNPROCESSABLE_ENTITY
    LOCKED = HTTPStatus.LOCKED
    FAILED_DEPENDENCY = HTTPStatus.FAILED_DEPENDENCY
    UPGRADE_REQUIRED = HTTPStatus.UPGRADE_REQUIRED
    PRECONDITION_REQUIRED = HTTPStatus.PRECONDITION_REQUIRED
    TOO_MANY_REQUESTS = HTTPStatus.TOO_MANY_REQUESTS
    REQUEST_HEADER_FIELDS_TOO_LARGE = HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE
    INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR
    NOT_IMPLEMENTED = HTTPStatus.NOT_IMPLEMENTED
    BAD_GATEWAY = HTTPStatus.BAD_GATEWAY
    SERVICE_UNAVAILABLE = HTTPStatus.SERVICE_UNAVAILABLE
    GATEWAY_TIMEOUT = HTTPStatus.GATEWAY_TIMEOUT
    HTTP_VERSION_NOT_SUPPORTED = HTTPStatus.HTTP_VERSION_NOT_SUPPORTED
    VARIANT_ALSO_NEGOTIATES = HTTPStatus.VARIANT_ALSO_NEGOTIATES
    INSUFFICIENT_STORAGE = HTTPStatus.INSUFFICIENT_STORAGE
    LOOP_DETECTED = HTTPStatus.LOOP_DETECTED
    NOT_EXTENDED = HTTPStatus.NOT_EXTENDED
    NETWORK_AUTHENTICATION_REQUIRED = HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED
    """
        )
    )


astroid.register_module_extender(astroid.MANAGER, "http.client", _http_transform)
