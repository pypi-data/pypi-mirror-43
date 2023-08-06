#!/usr/bin/env python3

import asyncio
import os

from gv_services.proto.common_pb2 import Ack
from gv_services.proto.geographer_pb2 import Locations, Mapping
from gv_services.storage.dbstorage.dbstorage import DbStorage
from gv_services.settings import SHAPEFILE_NAME
from gv_utils import enums


ATT = enums.AttId.att
EID = enums.AttId.eid
GEOM = enums.AttId.geom
WEBATT = enums.AttId.webatt


class Geographer:

    def __init__(self, logger, basecartopath, *dbcredentials):
        super().__init__()
        self.logger = logger
        self.basecartopath = basecartopath
        self.dbstorage = DbStorage(*dbcredentials)

    async def async_init(self):
        await self.dbstorage.async_init()

    async def import_shapefile_to_db(self, stream):
        await asyncio.gather(stream.send_message(Ack(success=True)),
                             self.dbstorage.import_shapefile(os.path.join(self.basecartopath, SHAPEFILE_NAME)))

    async def get_data_points(self, stream):
        message = await stream.recv_message()
        eids, datatype = message.eids, message.datatype
        datapoints = {}
        for v in (await self.dbstorage.get_data_points(eids, datatype)).values():
            datapoints.update(v)
        datapoints = await Geographer._locations_to_protobuf(datapoints)
        await stream.send_message(datapoints, end=True)

    async def get_roads(self, stream):
        message = await stream.recv_message()
        eids = message.eids
        roads = await Geographer._locations_to_protobuf(await self.dbstorage.get_roads(eids))
        await stream.send_message(roads, end=True)

    async def get_zones(self, stream):
        message = await stream.recv_message()
        eids = message.eids
        zones = await Geographer._locations_to_protobuf(await self.dbstorage.get_zones(eids))
        await stream.send_message(zones, end=True)

    # TODO: impl validat

    async def get_mapping_roads_data_points(self, stream):
        message = await stream.recv_message()
        roadeids, dpeids, validat = message.fromeids, message.toeids, message.validat.ToSeconds()
        roadsdatapoints = await Geographer._mappings_to_protobuf(await self.dbstorage.get_mapping_roads_data_points(
            roadeids, dpeids, validat))
        roadsdatapoints.validat.FromSeconds(validat)
        await stream.send_message(roadsdatapoints, end=True)

    async def get_mapping_zones_roads(self, stream):
        message = await stream.recv_message()
        roadeids, dpeids, validat = message.fromeids, message.toeids, message.validat.ToSeconds()
        zonesroads = await Geographer._mappings_to_protobuf(await self.dbstorage.get_mapping_zones_roads(
            roadeids, dpeids, validat))
        zonesroads.validat.FromSeconds(validat)
        await stream.send_message(zonesroads, end=True)

    async def update_roads_freeflow_speed(self, stream):
        pass

    async def update_zones_freeflow_speed(self, stream):
        pass

    @staticmethod
    async def _locations_to_protobuf(locations):
        def sync_func():
            pblocations = Locations()
            for eid, loc in locations.items():
                pblocations.locations[eid].geom = loc[GEOM].wkb
                pblocations.locations[eid].att.ToJsonString(loc[ATT])
                pblocations.locations[eid].webatt.ToJsonString(loc[WEBATT])
            return pblocations
        return await asyncio.get_event_loop().run_in_executor(None, sync_func)

    @staticmethod
    async def _mappings_to_protobuf(mapping):
        def sync_func():
            pbmapping = Mapping()
            for fromeid, toeids in mapping.items():
                pbmapping.mapping[fromeid].eids.extend(toeids)
            return pbmapping
        return await asyncio.get_event_loop().run_in_executor(None, sync_func)
