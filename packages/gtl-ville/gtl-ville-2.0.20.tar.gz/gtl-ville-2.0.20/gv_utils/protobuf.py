#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio
from concurrent.futures import ProcessPoolExecutor
import io

from gv_services.proto.common_pb2 import TrafficData
from gv_services.proto.geographer_pb2 import Locations, Mapping
from gv_utils import csv, enums, geometry


ATT = enums.AttId.att
EID = enums.AttId.eid
GEOM = enums.AttId.geom
WEBATT = enums.AttId.webatt


async def encode_traffic_data(trafficdata):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        trafficdata = await loop.run_in_executor(pool, _csv_dumps_bytes, *(trafficdata,))
    return TrafficData(data=trafficdata)


def _csv_dumps_bytes(data):
    return csv.dumps(data).getvalue()


async def decode_traffic_data(response):
    data = response.data
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        data = await loop.run_in_executor(pool, _csv_loads_bytes, *(data,))
    return data


def _csv_loads_bytes(data):
    return csv.loads(io.BytesIO(data))


async def encode_locations(locations):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        locations = await loop.run_in_executor(pool, _encode_locations, *(locations,))
    return locations


def _encode_locations(locations):
    pblocations = Locations()
    for eid, loc in locations.items():
        pblocations.locations[eid].geom = loc[GEOM].wkb
        pblocations.locations[eid].att.ToJsonString(loc[ATT])
        pblocations.locations[eid].webatt.ToJsonString(loc[WEBATT])
    return pblocations


async def decode_locations(response):
    loop = asyncio.get_event_loop()
    locations = await loop.run_in_executor(None, _decode_locations, *(response.locations,))
    return locations


def _decode_locations(pblocations):
    locations = {}
    for eid in pblocations:
        loc = pblocations[eid]
        locations[eid] = {EID: eid, GEOM: geometry.decode_geometry(loc.geom),
                          ATT: loc.att.FromJsonString(), WEBATT: loc.webatt.FromJsonString()}
    return locations


async def encode_mapping(mapping):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        mapping = await loop.run_in_executor(pool, _encode_mapping, *(mapping,))
    return mapping


def _encode_mapping(mapping):
    pbmapping = Mapping()
    for fromeid, toeids in mapping.items():
        pbmapping.mapping[fromeid].eids.extend(toeids)
    return pbmapping


async def decode_mapping(response):
    loop = asyncio.get_event_loop()
    mapping = await loop.run_in_executor(None, _decode_mapping, *(response.mapping,))
    return mapping


def _decode_mapping(pbmapping):
    mapping = {}
    for eid in pbmapping:
        mapping[eid] = pbmapping[eid].eids
    return mapping
