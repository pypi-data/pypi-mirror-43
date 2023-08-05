# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Network(pulumi.CustomResource):
    auto_create_subnetworks: pulumi.Output[bool]
    """
    If set to true, this network will be
    created in auto subnet mode, and Google will create a subnet for each region
    automatically. If set to false, a custom subnetted network will be created that
    can support `google_compute_subnetwork` resources. Defaults to true.
    """
    description: pulumi.Output[str]
    """
    A brief description of this resource.
    """
    gateway_ipv4: pulumi.Output[str]
    """
    The IPv4 address of the gateway.
    """
    ipv4_range: pulumi.Output[str]
    """
    If set to a CIDR block, uses the legacy VPC API with the
    specified range. This API is deprecated. If set, `auto_create_subnetworks` must be
    explicitly set to false.
    """
    name: pulumi.Output[str]
    """
    A unique name for the resource, required by GCE.
    Changing this forces a new resource to be created.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs. If it
    is not provided, the provider project is used.
    """
    routing_mode: pulumi.Output[str]
    """
    Sets the network-wide routing mode for Cloud Routers
    to use. Accepted values are `"GLOBAL"` or `"REGIONAL"`. Defaults to `"REGIONAL"`.
    Refer to the [Cloud Router documentation](https://cloud.google.com/router/docs/concepts/overview#dynamic-routing-mode)
    for more details.
    """
    self_link: pulumi.Output[str]
    """
    The URI of the created resource.
    """
    def __init__(__self__, resource_name, opts=None, auto_create_subnetworks=None, description=None, ipv4_range=None, name=None, project=None, routing_mode=None, __name__=None, __opts__=None):
        """
        Manages a network within GCE. For more information see
        [the official documentation](https://cloud.google.com/compute/docs/vpc)
        and
        [API](https://cloud.google.com/compute/docs/reference/latest/networks).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_create_subnetworks: If set to true, this network will be
               created in auto subnet mode, and Google will create a subnet for each region
               automatically. If set to false, a custom subnetted network will be created that
               can support `google_compute_subnetwork` resources. Defaults to true.
        :param pulumi.Input[str] description: A brief description of this resource.
        :param pulumi.Input[str] ipv4_range: If set to a CIDR block, uses the legacy VPC API with the
               specified range. This API is deprecated. If set, `auto_create_subnetworks` must be
               explicitly set to false.
        :param pulumi.Input[str] name: A unique name for the resource, required by GCE.
               Changing this forces a new resource to be created.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] routing_mode: Sets the network-wide routing mode for Cloud Routers
               to use. Accepted values are `"GLOBAL"` or `"REGIONAL"`. Defaults to `"REGIONAL"`.
               Refer to the [Cloud Router documentation](https://cloud.google.com/router/docs/concepts/overview#dynamic-routing-mode)
               for more details.
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

        __props__['auto_create_subnetworks'] = auto_create_subnetworks

        __props__['description'] = description

        __props__['ipv4_range'] = ipv4_range

        __props__['name'] = name

        __props__['project'] = project

        __props__['routing_mode'] = routing_mode

        __props__['gateway_ipv4'] = None
        __props__['self_link'] = None

        super(Network, __self__).__init__(
            'gcp:compute/network:Network',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

