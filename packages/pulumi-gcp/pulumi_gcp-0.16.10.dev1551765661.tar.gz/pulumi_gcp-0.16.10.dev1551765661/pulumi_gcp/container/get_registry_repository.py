# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetRegistryRepositoryResult:
    """
    A collection of values returned by getRegistryRepository.
    """
    def __init__(__self__, project=None, repository_url=None, id=None):
        if project and not isinstance(project, str):
            raise TypeError('Expected argument project to be a str')
        __self__.project = project
        if repository_url and not isinstance(repository_url, str):
            raise TypeError('Expected argument repository_url to be a str')
        __self__.repository_url = repository_url
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_registry_repository(project=None,region=None,opts=None):
    """
    This data source fetches the project name, and provides the appropriate URLs to use for container registry for this project.
    
    The URLs are computed entirely offline - as long as the project exists, they will be valid, but this data source does not contact Google Container Registry (GCR) at any point.
    """
    __args__ = dict()

    __args__['project'] = project
    __args__['region'] = region
    __ret__ = await pulumi.runtime.invoke('gcp:container/getRegistryRepository:getRegistryRepository', __args__, opts=opts)

    return GetRegistryRepositoryResult(
        project=__ret__.get('project'),
        repository_url=__ret__.get('repositoryUrl'),
        id=__ret__.get('id'))
