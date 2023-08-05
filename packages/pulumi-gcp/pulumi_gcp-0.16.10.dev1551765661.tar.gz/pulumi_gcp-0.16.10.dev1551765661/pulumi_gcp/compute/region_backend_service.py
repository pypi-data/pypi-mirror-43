# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class RegionBackendService(pulumi.CustomResource):
    backends: pulumi.Output[list]
    """
    The list of backends that serve this BackendService.
    Structure is documented below.
    """
    connection_draining_timeout_sec: pulumi.Output[int]
    """
    Time for which instance will be drained
    (not accept new connections, but still work to finish started ones). Defaults to `0`.
    """
    description: pulumi.Output[str]
    """
    The textual description for the backend service.
    """
    fingerprint: pulumi.Output[str]
    """
    The fingerprint of the backend service.
    """
    health_checks: pulumi.Output[str]
    """
    Specifies a list of health checks
    for checking the health of the backend service. Currently at most
    one health check can be specified, and a health check is required.
    """
    name: pulumi.Output[str]
    """
    The name of the backend service.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs. If it
    is not provided, the provider project is used.
    """
    protocol: pulumi.Output[str]
    """
    The protocol for incoming requests. Defaults to
    `TCP`.
    """
    region: pulumi.Output[str]
    """
    The Region in which the created address should reside.
    If it is not provided, the provider region is used.
    """
    self_link: pulumi.Output[str]
    """
    The URI of the created resource.
    """
    session_affinity: pulumi.Output[str]
    """
    How to distribute load. Options are `NONE` (no
    affinity), `CLIENT_IP`, `CLIENT_IP_PROTO`, or `CLIENT_IP_PORT_PROTO`.
    Defaults to `NONE`.
    """
    timeout_sec: pulumi.Output[int]
    """
    The number of secs to wait for a backend to respond
    to a request before considering the request failed. Defaults to `30`.
    """
    def __init__(__self__, resource_name, opts=None, backends=None, connection_draining_timeout_sec=None, description=None, health_checks=None, name=None, project=None, protocol=None, region=None, session_affinity=None, timeout_sec=None, __name__=None, __opts__=None):
        """
        A Region Backend Service defines a regionally-scoped group of virtual machines that will serve traffic for load balancing.
        For more information see [the official documentation](https://cloud.google.com/compute/docs/load-balancing/internal/)
        and [API](https://cloud.google.com/compute/docs/reference/latest/regionBackendServices).
        
        > **Note**: Region backend services can only be used when using internal load balancing. For external load balancing, use
          `google_compute_backend_service` instead.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] backends: The list of backends that serve this BackendService.
               Structure is documented below.
        :param pulumi.Input[int] connection_draining_timeout_sec: Time for which instance will be drained
               (not accept new connections, but still work to finish started ones). Defaults to `0`.
        :param pulumi.Input[str] description: The textual description for the backend service.
        :param pulumi.Input[str] health_checks: Specifies a list of health checks
               for checking the health of the backend service. Currently at most
               one health check can be specified, and a health check is required.
        :param pulumi.Input[str] name: The name of the backend service.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] protocol: The protocol for incoming requests. Defaults to
               `TCP`.
        :param pulumi.Input[str] region: The Region in which the created address should reside.
               If it is not provided, the provider region is used.
        :param pulumi.Input[str] session_affinity: How to distribute load. Options are `NONE` (no
               affinity), `CLIENT_IP`, `CLIENT_IP_PROTO`, or `CLIENT_IP_PORT_PROTO`.
               Defaults to `NONE`.
        :param pulumi.Input[int] timeout_sec: The number of secs to wait for a backend to respond
               to a request before considering the request failed. Defaults to `30`.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['backends'] = backends

        __props__['connection_draining_timeout_sec'] = connection_draining_timeout_sec

        __props__['description'] = description

        if health_checks is None:
            raise TypeError('Missing required property health_checks')
        __props__['health_checks'] = health_checks

        __props__['name'] = name

        __props__['project'] = project

        __props__['protocol'] = protocol

        __props__['region'] = region

        __props__['session_affinity'] = session_affinity

        __props__['timeout_sec'] = timeout_sec

        __props__['fingerprint'] = None
        __props__['self_link'] = None

        super(RegionBackendService, __self__).__init__(
            'gcp:compute/regionBackendService:RegionBackendService',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

