#!/usr/bin/env python3

import asyncio
import os

from gv_services.proto.common_pb2 import Ack
from gv_services.storage.dbstorage.dbstorage import DbStorage
from gv_services.settings import SHAPEFILE_NAME
from gv_utils import protobuf


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
        eids, datatype = message.eids.eids, message.datatype
        datapoints = {}
        for v in (await self.dbstorage.get_data_points(eids, datatype)).values():
            datapoints.update(v)
        datapoints = await protobuf.encode_locations(datapoints)
        await stream.send_message(datapoints, end=True)

    async def get_roads(self, stream):
        message = await stream.recv_message()
        eids = message.eids.eids
        roads = await protobuf.encode_locations(await self.dbstorage.get_roads(eids))
        await stream.send_message(roads, end=True)

    async def get_zones(self, stream):
        message = await stream.recv_message()
        eids = message.eids.eids
        zones = await protobuf.encode_locations(await self.dbstorage.get_zones(eids))
        await stream.send_message(zones, end=True)

    # TODO: impl validat

    async def get_mapping_roads_data_points(self, stream):
        message = await stream.recv_message()
        roadeids, dpeids, validat = message.fromeids.eids, message.toeids.eids, message.validat.ToSeconds()
        roadsdatapoints = await protobuf.encode_mapping(await self.dbstorage.get_mapping_roads_data_points(
            roadeids, dpeids, validat))
        roadsdatapoints.validat.FromSeconds(validat)
        await stream.send_message(roadsdatapoints, end=True)

    async def get_mapping_zones_roads(self, stream):
        message = await stream.recv_message()
        roadeids, dpeids, validat = message.fromeids.eids, message.toeids.eids, message.validat.ToSeconds()
        zonesroads = await protobuf.encode_mapping(await self.dbstorage.get_mapping_zones_roads(
            roadeids, dpeids, validat))
        zonesroads.validat.FromSeconds(validat)
        await stream.send_message(zonesroads, end=True)

    async def update_roads_freeflow_speed(self, stream):
        pass

    async def update_zones_freeflow_speed(self, stream):
        pass
