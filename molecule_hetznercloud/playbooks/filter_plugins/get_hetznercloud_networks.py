#!/usr/bin/env python
"""Usage:"""
""" loop: "{{ molecule_yml.platforms|molecule_get_hetznercloud_networks('networks') }}" """  # noqa
""" loop: "{{ molecule_yml.platforms|molecule_get_hetznercloud_networks('subnetworks') }}" """  # noqa


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def get_hetznercloud_networks(data, request):
    network_list = {}
    subnetwork_list = []

    if request == "networks":

        for platform in data:
            if "networks" in platform:
                for network in platform["networks"]:
                    values = network
                    del network["subnet"]
                    network_name = network['name']
                    if network_name in network_list:
                        network_list[network_name] = merge_two_dicts(
                            network_list[network_name], values
                        )
                    else:
                        network_list[network_name] = values

        return [x for x in network_list.values()]

    elif request == "subnetworks":

        for platform in data:
            name = platform["name"]
            if "networks" in platform:
                for network in platform["networks"]:
                    values = network
                    network_name = network['name']
                    if "subnet" in values:
                        values["subnet"]["server_name"] = name
                        values["subnet"]["network_name"] = network_name
                        subnetwork_list.append(values["subnet"])

        return subnetwork_list


class FilterModule(object):
    """Core Molecule filter plugins."""

    def filters(self):
        return {
            "molecule_get_hetznercloud_networks": get_hetznercloud_networks,
        }
