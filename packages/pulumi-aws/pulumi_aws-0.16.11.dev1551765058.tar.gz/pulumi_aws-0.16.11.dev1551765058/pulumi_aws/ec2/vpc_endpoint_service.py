# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class VpcEndpointService(pulumi.CustomResource):
    acceptance_required: pulumi.Output[bool]
    """
    Whether or not VPC endpoint connection requests to the service must be accepted by the service owner - `true` or `false`.
    """
    allowed_principals: pulumi.Output[list]
    """
    The ARNs of one or more principals allowed to discover the endpoint service.
    """
    availability_zones: pulumi.Output[list]
    """
    The Availability Zones in which the service is available.
    """
    base_endpoint_dns_names: pulumi.Output[list]
    """
    The DNS names for the service.
    """
    network_load_balancer_arns: pulumi.Output[list]
    """
    The ARNs of one or more Network Load Balancers for the endpoint service.
    """
    private_dns_name: pulumi.Output[str]
    """
    The private DNS name for the service.
    """
    service_name: pulumi.Output[str]
    """
    The service name.
    """
    service_type: pulumi.Output[str]
    """
    The service type, `Gateway` or `Interface`.
    """
    state: pulumi.Output[str]
    """
    The state of the VPC endpoint service.
    """
    def __init__(__self__, resource_name, opts=None, acceptance_required=None, allowed_principals=None, network_load_balancer_arns=None, __name__=None, __opts__=None):
        """
        Provides a VPC Endpoint Service resource.
        Service consumers can create an _Interface_ VPC Endpoint to connect to the service.
        
        > **NOTE on VPC Endpoint Services and VPC Endpoint Service Allowed Principals:** Terraform provides
        both a standalone VPC Endpoint Service Allowed Principal resource
        and a VPC Endpoint Service resource with an `allowed_principals` attribute. Do not use the same principal ARN in both
        a VPC Endpoint Service resource and a VPC Endpoint Service Allowed Principal resource. Doing so will cause a conflict
        and will overwrite the association.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] acceptance_required: Whether or not VPC endpoint connection requests to the service must be accepted by the service owner - `true` or `false`.
        :param pulumi.Input[list] allowed_principals: The ARNs of one or more principals allowed to discover the endpoint service.
        :param pulumi.Input[list] network_load_balancer_arns: The ARNs of one or more Network Load Balancers for the endpoint service.
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

        if acceptance_required is None:
            raise TypeError('Missing required property acceptance_required')
        __props__['acceptance_required'] = acceptance_required

        __props__['allowed_principals'] = allowed_principals

        if network_load_balancer_arns is None:
            raise TypeError('Missing required property network_load_balancer_arns')
        __props__['network_load_balancer_arns'] = network_load_balancer_arns

        __props__['availability_zones'] = None
        __props__['base_endpoint_dns_names'] = None
        __props__['private_dns_name'] = None
        __props__['service_name'] = None
        __props__['service_type'] = None
        __props__['state'] = None

        super(VpcEndpointService, __self__).__init__(
            'aws:ec2/vpcEndpointService:VpcEndpointService',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

