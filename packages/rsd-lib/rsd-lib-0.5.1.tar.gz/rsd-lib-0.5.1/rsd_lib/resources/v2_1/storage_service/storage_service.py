# Copyright 2017 Intel, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from sushy.resources import base
from sushy import utils

from rsd_lib import common as rsd_lib_common
from rsd_lib.resources.v2_1.storage_service import logical_drive
from rsd_lib.resources.v2_1.storage_service import physical_drive
from rsd_lib.resources.v2_1.storage_service import remote_target

LOG = logging.getLogger(__name__)


class StorageService(base.ResourceBase):

    description = base.Field('Description')
    """The storage service description"""

    identity = base.Field('Id', required=True)
    """The storage service identity string"""

    name = base.Field('Name')
    """The storage service name"""

    status = rsd_lib_common.StatusField('Status')
    """The storage service status"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a StorageService

        :param connector: A Connector instance
        :param identity: The identity of the StorageService resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StorageService, self).__init__(connector, identity,
                                             redfish_version)

    def _get_logical_drive_collection_path(self):
        """Helper function to find the LogicalDriveCollection path"""
        return utils.get_sub_resource_path_by(self, 'LogicalDrives')

    @property
    @utils.cache_it
    def logical_drives(self):
        """Property to provide reference to `LogicalDriveCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        return logical_drive.LogicalDriveCollection(
            self._conn, self._get_logical_drive_collection_path(),
            redfish_version=self.redfish_version)

    def _get_physical_drive_collection_path(self):
        """Helper function to find the PhysicalDriveCollection path"""
        return utils.get_sub_resource_path_by(self, 'Drives')

    @property
    @utils.cache_it
    def physical_drives(self):
        """Property to provide reference to `PhysicalDriveCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        return physical_drive.PhysicalDriveCollection(
            self._conn, self._get_physical_drive_collection_path(),
            redfish_version=self.redfish_version)

    def _get_remote_target_collection_path(self):
        """Helper function to find the RemoteTargetCollection path"""
        return utils.get_sub_resource_path_by(self, 'RemoteTargets')

    @property
    @utils.cache_it
    def remote_targets(self):
        """Property to provide reference to `RemoteTargetCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        return remote_target.RemoteTargetCollection(
            self._conn, self._get_remote_target_collection_path(),
            redfish_version=self.redfish_version)


class StorageServiceCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return StorageService

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a StorageServiceCollection

        :param connector: A Connector instance
        :param path: The canonical path to the StorageService collection
            resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StorageServiceCollection, self).__init__(connector, path,
                                                       redfish_version)
