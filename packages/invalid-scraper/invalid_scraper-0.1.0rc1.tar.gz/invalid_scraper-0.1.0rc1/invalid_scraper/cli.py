#!/usr/bin/env python
# Copyright (c) 2019 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""invalid_scraper cli entry point."""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import getpass
import os
import re
import sys

import napalm
import yaml


def main():  # pragma: no cover
    """Excecute the invalid_scraper cli tool."""
    try:
        default_user = os.environ["USER"]
    except KeyError:
        default_user = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", "-d", type=str, default="wolcomm.net")
    parser.add_argument("--username", "-u",
                        type=str, default=default_user,
                        required=(not default_user))
    args = parser.parse_args()
    password = getpass.getpass(prompt="Password for {}: ".format(args.username))  # noqa
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(data_dir, "hosts.yml")) as f:
        data = yaml.load(f)
    for host in data["hosts"]:
        driver = napalm.get_network_driver("ios")
        with driver(hostname="{}.{}".format(host, args.domain),
                    username=args.username, password=password) as device:
            print("Searching {}".format(host))
            neighbors = device.get_bgp_neighbors()
            for peer, peer_data in neighbors["global"]["peers"].items():
                if not re.match(r"^[A-Z]{3}\d{2}\s", peer_data["description"]):
                    continue
                cmd_template = "show bgp {} unicast neighbor {} received-routes | inc ^I"  # noqa
                for af, prefixes in peer_data["address_family"].items():
                    if prefixes["received_prefixes"] <= 0:
                        continue
                    cmd = cmd_template.format(af, peer)
                    output = device.cli([cmd])
                    if output[cmd]:
                        print("{}: {}".format(peer, peer_data["description"]))
                        print(output[cmd])
    return


if __name__ == "__main__":
    sys.exit(main())
