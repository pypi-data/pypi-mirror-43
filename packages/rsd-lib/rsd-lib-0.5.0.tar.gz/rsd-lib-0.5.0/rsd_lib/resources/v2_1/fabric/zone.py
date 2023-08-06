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
from rsd_lib.resources.v2_1.fabric import endpoint

LOG = logging.getLogger(__name__)


class ZoneLinksField(base.CompositeField):
    endpoint_identities = base.Field('Endpoints', default=[],
                                     adapter=utils.get_members_identities)
    """An array of references to the endpoints
       that are contained in this zone
    """

    involved_switches = base.Field('InvolvedSwitches', default=[],
                                   adapter=utils.get_members_identities)
    """An array of references to the switchs
       that are utilized in this zone
    """


class Zone(base.ResourceBase):
    description = base.Field('Description')
    """The zone description"""

    identity = base.Field('Id', required=True)
    """The zone identity string"""

    name = base.Field('Name')
    """The zone name"""

    links = ZoneLinksField('Links')
    """The zone links"""

    status = rsd_lib_common.StatusField('Status')
    """The zone status"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Zone

        :param connector: A Connector instance
        :param identity: The identity of the Zone resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Zone, self).__init__(connector, identity,
                                   redfish_version)

    @property
    @utils.cache_it
    def endpoints(self):
        """Return a list of Endpoints present in the Zone

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        return [
            endpoint.Endpoint(self._conn, id_, self.redfish_version)
            for id_ in self.links.endpoint_identities]

    def update(self, endpoints):
        """Add or remove Endpoints from a Zone

        User have to provide a full representation of Endpoints array. A
        partial update (single element update/append/detele) is not supported.
        :param endpoints: a full representation of Endpoints array
        """
        data = {"Endpoints": []}
        data['Endpoints'] = [{'@odata.id': endpoint} for endpoint in endpoints]

        self._conn.patch(self.path, data=data)


class ZoneCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Zone

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a Zone Collection

        :param connector: A Connector instance
        :param path: The canonical path to the Zone collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(ZoneCollection, self).__init__(connector, path,
                                             redfish_version)
