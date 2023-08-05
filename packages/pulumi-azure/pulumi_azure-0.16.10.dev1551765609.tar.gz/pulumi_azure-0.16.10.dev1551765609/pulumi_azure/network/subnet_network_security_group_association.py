# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class SubnetNetworkSecurityGroupAssociation(pulumi.CustomResource):
    network_security_group_id: pulumi.Output[str]
    """
    The ID of the Network Security Group which should be associated with the Subnet. Changing this forces a new resource to be created.
    """
    subnet_id: pulumi.Output[str]
    """
    The ID of the Subnet. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, network_security_group_id=None, subnet_id=None, __name__=None, __opts__=None):
        """
        Associates a Network Security Group with a Subnet within a Virtual Network.
        
        > **NOTE:** Subnet `<->` Network Security Group associations currently need to be configured on both this resource and using the `network_security_group_id` field on the `azurerm_subnet` resource. The next major version of the AzureRM Provider (2.0) will remove the `network_security_group_id` field from the `azurerm_subnet` resource such that this resource is used to link resources in future.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] network_security_group_id: The ID of the Network Security Group which should be associated with the Subnet. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subnet_id: The ID of the Subnet. Changing this forces a new resource to be created.
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

        if network_security_group_id is None:
            raise TypeError('Missing required property network_security_group_id')
        __props__['network_security_group_id'] = network_security_group_id

        if subnet_id is None:
            raise TypeError('Missing required property subnet_id')
        __props__['subnet_id'] = subnet_id

        super(SubnetNetworkSecurityGroupAssociation, __self__).__init__(
            'azure:network/subnetNetworkSecurityGroupAssociation:SubnetNetworkSecurityGroupAssociation',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

