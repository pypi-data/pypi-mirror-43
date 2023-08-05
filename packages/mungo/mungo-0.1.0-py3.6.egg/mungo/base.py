import os
from collections import defaultdict
from subprocess import run

from pulp import *
from yaml import safe_load

from mungo.repodata import Repodata, merge_repodata, get_repository_data
from mungo.solver import create_node, reduce_dag


def nodes_to_install(channels, packages, create_new_environment=False, njobs=4):
    if not create_new_environment:
        local_repodata = [Repodata.from_environment(os.getenv('CONDA_PREFIX'))]
    else:
        local_repodata = []

    repodata_chunks = get_repository_data(channels, njobs)
    repodata = merge_repodata(local_repodata + repodata_chunks)

    # add installed packages to the repodata

    default_packages = {"sqlite", "wheel", "pip"}

    all_nodes = defaultdict(dict)
    root = create_node("root", "", repodata, all_nodes=all_nodes,
                       override_dependencies=list(packages | default_packages))

    # create ILP problem
    prob = LpProblem("DependencySolve", LpMaximize)

    # reduce DAG
    reduce_dag(all_nodes)

    # build LP on the reduced DAG
    objective = []
    prob += root.x == 1
    for name, versions in all_nodes.items():
        # constraint: install exactly one version of a package (inluding pseudo no_install)
        no_install = LpVariable("{name}-no_install".format(name=name), 0, 1, LpInteger)
        prob += sum([n.x for n in versions.values()] + [no_install]) == 1

        # constraint: if a parent is installed, one version of each dependency must be installed too
        for current_node in versions.values():
            for out_group in current_node._out_nodes.values():
                prob += sum([n.x for n in out_group]) >= current_node.x

        # for n in versions.values():
        #     print(n.factor, n.normalized_version, n.name, n.version)
        # storing the objectives
        objective.extend([n.factor * n.normalized_version * n.x for n in versions.values()])
        #print([(n.name, n.normalized_version, n.factor) for n in versions.values()])

        if current_node is root: #no no_install for root
            continue

        max_normalized_version = max([n.normalized_version for n in versions.values() if n.normalized_version != 1] + [0])
        max_factor = max([n.factor for n in versions.values()])
        no_install_factor = (max_normalized_version + 1) * max_factor # install factor between max and no_install

        objective.append(no_install_factor * no_install)

    prob += sum(objective)
    prob.writeLP("WhiskasModel.lp")
    prob.solve()

    # TODO: catch unsolvable!!!
    #print(LpStatus[prob.status])

    # for v in prob.variables():
    #     print(v.name, v.varValue)


    # collect all install nodes
    install_nodes = []
    for _, versions in sorted(all_nodes.items()):
        for n in versions.values():
            if n.p is None:  # skip root
                continue
            x = n.x
            if x.varValue == 1.0 and not x.name.endswith("_no_install"):
                install_nodes.append(n)

    return sorted(install_nodes, key=lambda x: x.factor)


def read_environment_description(yml):
    with open(yml, 'rt') as reader:
        data = safe_load(reader)
        name = data.get('name', None)
        channels = data.get('channels', [])
        package_specs = {p for p in data.get('dependencies', []) if isinstance(p, str)}
        pip_specs = [p['pip'] for p in data.get('dependencies', []) if isinstance(p, dict) and 'pip' in p]
        pip_specs = {item for sublist in pip_specs for item in sublist}
        return name, channels, package_specs, pip_specs


def _get_condarc_channels():
    with open(os.path.expanduser(os.path.join('~', '.condarc')), 'rt') as reader:
        channels = safe_load(reader)
        return channels['channels']


def _install_prompt(to_install):
    print("The following packages will be INSTALLED:\n")
    for n in to_install:
        n.p['version_build'] = n.p['version'] + '-' + n.p['build']
        n.p['reponame'] = n.p['channel'].split('/')[-2]
    widths = {t: max([len(n.p[t]) for n in to_install])
              for t in ['name', 'version_build', 'reponame']}
    for n in sorted(to_install, key=lambda x: x.factor):
        if "installed" not in n.p:
            print("\t{:<{name_width}} {:<{version_width}} {:<{repo_width}}"
                  .format(n.p['name'], n.p['version_build'], n.p['reponame'],
                          name_width=widths['name'],
                          version_width=widths['version_build'],
                          repo_width=widths['reponame']))
    answer = input("\nProceed ([y]/n)? ")
    if answer not in {'\n', 'y'}:
        return False
    return True


def create_environment(name, channels, packages, pip, jobs=1):
    to_install = nodes_to_install(channels, packages, create_new_environment=True, njobs=jobs)
    if _install_prompt(to_install):
        command = "@EXPLICIT\n"
        command += '\n'.join([f'{n.p["channel"]}/{n.p["fn"]}' for n in to_install])
        ps = run(f'bash -i -c "conda create --name {name} --file /dev/stdin"', input=command.encode(), shell=True)


def install_packages(name, channels, packages, pip, jobs=1):
    to_install = [n for n in nodes_to_install(channels, packages, create_new_environment=False, njobs=jobs)
                  if "installed" not in n.p]
    if _install_prompt(to_install):
        command = "@EXPLICIT\n"
        command += '\n'.join([f'{n.p["channel"]}/{n.p["fn"]}' for n in to_install])
        ps = run('bash -i -c "conda install --file /dev/stdin"', input=command.encode(), shell=True)

# def installed_packages():
#     ps = run('bash -i -c "conda list"', shell=True, stdout=subprocess.PIPE)
#     for line in ps.stdout.decode().split("\n"):
#         if line.startswith("#"):
#             continue
#
#         split = line.split()
#         if len(split)<3:
#             continue
#
#         name, version, build = line.split()[:3]
#         yield (name, version, build)


#    repodata = merge_repodata([local_repodata] + repodata_chunks)
