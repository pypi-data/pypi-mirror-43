# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class HostedPublicVirtualInterface(pulumi.CustomResource):
    address_family: pulumi.Output[str]
    """
    The address family for the BGP peer. `ipv4 ` or `ipv6`.
    """
    amazon_address: pulumi.Output[str]
    """
    The IPv4 CIDR address to use to send traffic to Amazon. Required for IPv4 BGP peers.
    """
    arn: pulumi.Output[str]
    """
    The ARN of the virtual interface.
    """
    bgp_asn: pulumi.Output[int]
    """
    The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
    """
    bgp_auth_key: pulumi.Output[str]
    """
    The authentication key for BGP configuration.
    """
    connection_id: pulumi.Output[str]
    """
    The ID of the Direct Connect connection (or LAG) on which to create the virtual interface.
    """
    customer_address: pulumi.Output[str]
    """
    The IPv4 CIDR destination address to which Amazon should send traffic. Required for IPv4 BGP peers.
    """
    name: pulumi.Output[str]
    """
    The name for the virtual interface.
    """
    owner_account_id: pulumi.Output[str]
    """
    The AWS account that will own the new virtual interface.
    """
    route_filter_prefixes: pulumi.Output[list]
    """
    A list of routes to be advertised to the AWS network in this region.
    """
    vlan: pulumi.Output[int]
    """
    The VLAN ID.
    """
    def __init__(__self__, resource_name, opts=None, address_family=None, amazon_address=None, bgp_asn=None, bgp_auth_key=None, connection_id=None, customer_address=None, name=None, owner_account_id=None, route_filter_prefixes=None, vlan=None, __name__=None, __opts__=None):
        """
        Provides a Direct Connect hosted public virtual interface resource. This resource represents the allocator's side of the hosted virtual interface.
        A hosted virtual interface is a virtual interface that is owned by another AWS account.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_family: The address family for the BGP peer. `ipv4 ` or `ipv6`.
        :param pulumi.Input[str] amazon_address: The IPv4 CIDR address to use to send traffic to Amazon. Required for IPv4 BGP peers.
        :param pulumi.Input[int] bgp_asn: The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        :param pulumi.Input[str] bgp_auth_key: The authentication key for BGP configuration.
        :param pulumi.Input[str] connection_id: The ID of the Direct Connect connection (or LAG) on which to create the virtual interface.
        :param pulumi.Input[str] customer_address: The IPv4 CIDR destination address to which Amazon should send traffic. Required for IPv4 BGP peers.
        :param pulumi.Input[str] name: The name for the virtual interface.
        :param pulumi.Input[str] owner_account_id: The AWS account that will own the new virtual interface.
        :param pulumi.Input[list] route_filter_prefixes: A list of routes to be advertised to the AWS network in this region.
        :param pulumi.Input[int] vlan: The VLAN ID.
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

        if address_family is None:
            raise TypeError('Missing required property address_family')
        __props__['address_family'] = address_family

        __props__['amazon_address'] = amazon_address

        if bgp_asn is None:
            raise TypeError('Missing required property bgp_asn')
        __props__['bgp_asn'] = bgp_asn

        __props__['bgp_auth_key'] = bgp_auth_key

        if connection_id is None:
            raise TypeError('Missing required property connection_id')
        __props__['connection_id'] = connection_id

        __props__['customer_address'] = customer_address

        __props__['name'] = name

        if owner_account_id is None:
            raise TypeError('Missing required property owner_account_id')
        __props__['owner_account_id'] = owner_account_id

        if route_filter_prefixes is None:
            raise TypeError('Missing required property route_filter_prefixes')
        __props__['route_filter_prefixes'] = route_filter_prefixes

        if vlan is None:
            raise TypeError('Missing required property vlan')
        __props__['vlan'] = vlan

        __props__['arn'] = None

        super(HostedPublicVirtualInterface, __self__).__init__(
            'aws:directconnect/hostedPublicVirtualInterface:HostedPublicVirtualInterface',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

