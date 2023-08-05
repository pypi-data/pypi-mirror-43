# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class StoreFile(pulumi.CustomResource):
    account_name: pulumi.Output[str]
    """
    Specifies the name of the Data Lake Store for which the File should created.
    """
    local_file_path: pulumi.Output[str]
    """
    The path to the local file to be added to the Data Lake Store.
    """
    remote_file_path: pulumi.Output[str]
    """
    The path created for the file on the Data Lake Store.
    """
    def __init__(__self__, resource_name, opts=None, account_name=None, local_file_path=None, remote_file_path=None, __name__=None, __opts__=None):
        """
        Manage a Azure Data Lake Store File.
        
        > **Note:** If you want to change the data in the remote file without changing the `local_file_path`, then 
        taint the resource so the `azurerm_data_lake_store_file` gets recreated with the new data.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Specifies the name of the Data Lake Store for which the File should created.
        :param pulumi.Input[str] local_file_path: The path to the local file to be added to the Data Lake Store.
        :param pulumi.Input[str] remote_file_path: The path created for the file on the Data Lake Store.
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

        if account_name is None:
            raise TypeError('Missing required property account_name')
        __props__['account_name'] = account_name

        if local_file_path is None:
            raise TypeError('Missing required property local_file_path')
        __props__['local_file_path'] = local_file_path

        if remote_file_path is None:
            raise TypeError('Missing required property remote_file_path')
        __props__['remote_file_path'] = remote_file_path

        super(StoreFile, __self__).__init__(
            'azure:datalake/storeFile:StoreFile',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

