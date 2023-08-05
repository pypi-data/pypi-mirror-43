# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetSharedImageResult(object):
    """
    A collection of values returned by getSharedImage.
    """
    def __init__(__self__, description=None, eula=None, identifiers=None, location=None, os_type=None, privacy_statement_uri=None, release_note_uri=None, tags=None, id=None):
        if description and not isinstance(description, str):
            raise TypeError('Expected argument description to be a str')
        __self__.description = description
        """
        The description of this Shared Image.
        """
        if eula and not isinstance(eula, str):
            raise TypeError('Expected argument eula to be a str')
        __self__.eula = eula
        """
        The End User Licence Agreement for the Shared Image.
        """
        if identifiers and not isinstance(identifiers, list):
            raise TypeError('Expected argument identifiers to be a list')
        __self__.identifiers = identifiers
        if location and not isinstance(location, str):
            raise TypeError('Expected argument location to be a str')
        __self__.location = location
        """
        The supported Azure location where the Shared Image Gallery exists.
        """
        if os_type and not isinstance(os_type, str):
            raise TypeError('Expected argument os_type to be a str')
        __self__.os_type = os_type
        """
        The type of Operating System present in this Shared Image.
        """
        if privacy_statement_uri and not isinstance(privacy_statement_uri, str):
            raise TypeError('Expected argument privacy_statement_uri to be a str')
        __self__.privacy_statement_uri = privacy_statement_uri
        """
        The URI containing the Privacy Statement for this Shared Image.
        """
        if release_note_uri and not isinstance(release_note_uri, str):
            raise TypeError('Expected argument release_note_uri to be a str')
        __self__.release_note_uri = release_note_uri
        """
        The URI containing the Release Notes for this Shared Image.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError('Expected argument tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags assigned to the Shared Image.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_shared_image(gallery_name=None, name=None, resource_group_name=None):
    """
    Use this data source to access information about an existing Shared Image within a Shared Image Gallery.
    
    > **NOTE** Shared Image Galleries are currently in Public Preview. You can find more information, including [how to register for the Public Preview here](https://azure.microsoft.com/en-gb/blog/announcing-the-public-preview-of-shared-image-gallery/).
    """
    __args__ = dict()

    __args__['galleryName'] = gallery_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __ret__ = await pulumi.runtime.invoke('azure:compute/getSharedImage:getSharedImage', __args__)

    return GetSharedImageResult(
        description=__ret__.get('description'),
        eula=__ret__.get('eula'),
        identifiers=__ret__.get('identifiers'),
        location=__ret__.get('location'),
        os_type=__ret__.get('osType'),
        privacy_statement_uri=__ret__.get('privacyStatementUri'),
        release_note_uri=__ret__.get('releaseNoteUri'),
        tags=__ret__.get('tags'),
        id=__ret__.get('id'))
