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
        args = _get_args()
        for host in args.hosts:
            print("Searching {}".format(host))
            for line in _search_host(host, **vars(args)):
                print(line)
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        print(e)
        return 2
    return


def _get_args():
    """Parse cli args and return."""
    # try and use the current username as default value
    try:
        default_user = os.environ["USER"]
    except KeyError:
        default_user = None
    # set the default data-file location
    default_data_dir = os.path.join(os.path.dirname(__file__), "data")
    # set up the cli args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", "-d", type=str, default="wolcomm.net")
    parser.add_argument("--username", "-u",
                        type=str, default=default_user,
                        required=(not default_user))
    parser.add_argument("--password", "-p", type=str)
    parser.add_argument("--hosts_file", type=argparse.FileType(),
                        default=os.path.join(default_data_dir, "hosts.yml"))
    parser.add_argument("--hosts", type=str, nargs="*")
    # get cli args
    args = parser.parse_args()
    # ask for a password if non was provided
    if not args.password:
        prompt = "Password for {}: ".format(args.username)
        args.password = getpass.getpass(prompt=prompt)
    # read hosts_file if hosts was not provided on the cli
    if not args.hosts:
        try:
            with args.hosts_file as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print("Cound not open {} for reading: {}".format(args.hosts_file, e))  # noqa
            raise
        args.hosts = data["hosts"]
    return args


def _search_host(host=None, domain=None,
                 username=None, password=None, **kwargs):
    """Find invalid customer routes received by host."""
    result = []
    driver = napalm.get_network_driver("ios")
    try:
        with driver(hostname="{}.{}".format(host, domain),
                    username=username, password=password) as device:
            neighbors = device.get_bgp_neighbors()
            for peer, peer_data in neighbors["global"]["peers"].items():
                if not re.match(r"^[A-Z]{3}\d{2}\s",
                                peer_data["description"]):
                    continue
                cmd_template = "show bgp {} unicast neighbor {} received-routes | inc ^I"  # noqa
                for af, prefixes in peer_data["address_family"].items():
                    if prefixes["received_prefixes"] <= 0:
                        continue
                    cmd = cmd_template.format(af, peer)
                    output = device.cli([cmd])
                    if output[cmd]:
                        result.append("{}: {}".format(peer, peer_data["description"]))  # noqa
                        result.append(output[cmd])
    except Exception as e:
        print("Failed to get results from {}: {}".format(host, e))
    return result


if __name__ == "__main__":
    sys.exit(main())
