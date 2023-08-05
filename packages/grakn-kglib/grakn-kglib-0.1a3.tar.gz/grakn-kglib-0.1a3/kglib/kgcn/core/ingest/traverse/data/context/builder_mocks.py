#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

import kglib.kgcn.core.ingest.traverse.data.context.neighbour as neighbour
import kglib.kgcn.core.ingest.traverse.data.context.builder as builder


def gen(elements):
    for el in elements:
        yield el


def mock_traversal_output():
    c = builder.ThingContext(
        neighbour.Thing("0", "person", "entity"),
        [
            builder.Neighbour("employee", neighbour.TARGET_PLAYS, builder.ThingContext(
                neighbour.Thing("1", "employment", "relation"),
                [
                    builder.Neighbour("employer", neighbour.NEIGHBOUR_PLAYS, builder.ThingContext(
                        neighbour.Thing("2", "company", "entity"), []
                    )),
                ]
            )),
            builder.Neighbour("@has-name-owner", neighbour.TARGET_PLAYS, builder.ThingContext(
                neighbour.Thing("3", "@has-name", "relation"),
                [
                    builder.Neighbour("@has-name-value", neighbour.NEIGHBOUR_PLAYS, builder.ThingContext(
                        neighbour.Thing("4", "name", "attribute", data_type='string', value="Employee Name"),
                        []
                    )),
                ]
            ))

        ])
    return c


def _build_data(role_label, role_direction, neighbour_id, neighbour_type, neighbour_metatype, data_type=None,
                value=None):
    return {'role_label': role_label, 'role_direction': role_direction,
            'neighbour_thing': neighbour.Thing(neighbour_id, neighbour_type, neighbour_metatype, data_type=data_type,
                                               value=value)}


class MockNeighbourFinder:

    def find(self, thing_id, tx):

        if thing_id == "0":

            role_direction = neighbour.TARGET_PLAYS
            yield from gen([
                _build_data("employee", role_direction, "1", "employment", "relation"),
                _build_data("@has-name-owner", role_direction, "3", "@has-name", "relation")
            ])

        elif thing_id == "1":

            role_direction = neighbour.NEIGHBOUR_PLAYS
            yield from gen([_build_data("employer", role_direction, "2", "company", "entity")])

        elif thing_id == "3":

            role_direction = neighbour.NEIGHBOUR_PLAYS
            yield from gen([_build_data("@has-name-value", role_direction, "4", "name", "attribute",
                                        data_type='string', value="Employee Name")])

        else:
            raise ValueError("This concept id hasn't been mocked")
