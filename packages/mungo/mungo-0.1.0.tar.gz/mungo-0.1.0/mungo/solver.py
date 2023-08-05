import re

from collections import defaultdict
from functools import partial
from pulp import *

from packaging.version import parse as vparse

operator_function = dict()
operator_function[">="] = lambda x, y: x >= y
operator_function[">"] = lambda x, y: x > y
operator_function["<="] = lambda x, y: x <= y
operator_function["<"] = lambda x, y: x < y
operator_function["!="] = lambda x, y: x != y
operator_function["="] = lambda x, y: x == y


class Node():
    def __init__(self, name, version, factor, p):
        self.name = name
        self.version = version
        self.factor = factor
        self._in_nodes = []
        self._out_nodes = defaultdict(list)
        self._x = None
        self.p = p

    def delete(self):
        for n in self.in_nodes:
            n.out_nodes.remove(self.current_node)
        for n in self.out_nodes:
            n.in_nodes.remove(self.current_node)

    def add_in_node(self, n):
        self._in_nodes.append(n)

    def remove_in_node(self, n):
        self._in_nodes.remove(n)

    def add_out_node(self, n):
        self._out_nodes[n.name].append(n)

    def remove_out_node(self, n):
        self._out_nodes[n.name].remove(n)

    @property
    def normalized_version(self):
        if self.p is None:
            return 1.0
        return self.p["normalized_version"]

    @property
    def in_nodes(self):
        return self._in_nodes

    @property
    def out_nodes(self):
        for nodes in self._out_nodes.values():
            for n in nodes:
                yield n

    @property
    def x(self):
        # create LP variable, if not exist
        if self._x is None:
            self._x = LpVariable("{name}-{version}".format(name=self.name, version=self.version), 0, 1, LpInteger)
        return self._x

    def delete(self):
        for n in self.in_nodes:
            n.remove_out_node(self)
        for n in self.out_nodes:
            n.remove_in_node(self)


def valid_packages(s, repodata):
    split = re.split('(!=|>=|<=|=|<|>| )', s)
    split = [s for s in split if not s == " " and len(s)]

    if len(split) == 5:
        name, operator1, version1, operator2, version2 = split
        is_valid = lambda x: partial(operator_function[operator1], y=vparse(version1))(vparse(x)) and partial(
            operator_function[operator2], y=vparse(version2))(vparse(x))
    elif len(split) == 3:
        # version constraint
        name, operator, version = split
        if operator in [">=", ">", "<=", "<", "!=", "="]:
            is_valid = lambda x: partial(operator_function[operator], y=vparse(version))(vparse(x))
        else:
            # version build constraint
            name, version, build = split
            is_valid = lambda x: partial(operator_function["="], y=vparse(version))(vparse(x))
    elif len(split) == 2:
        # version constraint without operator (equals ==)
        name, version = split
        is_valid = lambda x: partial(operator_function["="], y=vparse(version))(vparse(x))
    elif len(split) == 1:
        # no version constraint
        name, = split
        is_valid = lambda x: True
    else:
        raise Exception("invalid version constraint")

    for v in repodata.d[name]:
        if is_valid(v):
            yield (name, v)


def create_node(name, version, repodata,
                factor=1000,
                sender=None,
                all_nodes=defaultdict(dict),
                override_dependencies=None):
    if version in all_nodes[name]:
        node = all_nodes[name][version]
        node.add_in_node(sender)  # add the parent to in-nodes
        return node

    # create new node
    if version in repodata.d[name]:
        p = repodata.d[name][version]
    else:
        p = None

    new_node = Node(name, version, factor, p)

    if sender is not None:
        new_node.add_in_node(sender)

    all_nodes[name][version] = new_node

    # get package information from repodata
    if override_dependencies is not None:
        dependencies = override_dependencies
    else:
        dependencies = p["depends"]

    for dependency in dependencies:
        for d_name, d_version in valid_packages(dependency, repodata):
            d_node = create_node(d_name, d_version, repodata, factor / 10, new_node, all_nodes)
            new_node.add_out_node(d_node)
    return new_node


def reduce_dag(all_nodes):
    # reduce DAG
    for name, versions in all_nodes.items():
        seen_keys = set()
        for version in sorted(versions, key=lambda v: versions[v].normalized_version, reverse=True):
            current_node = versions[version]
            in_node_key = tuple(sorted([(n.name, n.version) for n in current_node.in_nodes]))
            out_node_key = tuple(sorted([(n.name, n.version) for n in current_node.out_nodes]))
            key = (in_node_key, out_node_key)
            if key in seen_keys:
                # the in-node out-node combination exist in a higher version of the same package
                # thus the higher version is ALWAYS preferable and this version can be removed
                current_node.delete()
                del (all_nodes[name][version])
            else:
                seen_keys.add(key)
