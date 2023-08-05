import argparse
import sys

from mungo.base import create_environment, install_packages, read_environment_description, _get_condarc_channels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jobs", help="number of jobs", default=4)

    subparsers = parser.add_subparsers(title='subcommands',
                                       dest='command',
                                       description='valid subcommands',
                                       help='additional help')
    subparsers.required = True

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument("-n", "--name", help="the name of the environment")
    parser_create.add_argument("package_spec", nargs="*")
    parser_create.add_argument("--file", metavar="FILE", default=None)
    parser_create.add_argument("--channel", "-c", nargs=1, action="append", metavar="CHANNEL", default=[])

    parser_install = subparsers.add_parser('install')
    parser_install.add_argument("-n", "--name", help="the name of the environment", default=None)
    parser_install.add_argument("package_spec", nargs="+")
    parser_install.add_argument("--file", metavar="FILE", default=None)
    parser_install.add_argument("--channel", "-c", nargs=1, action="append", metavar="CHANNEL", default=[])

    args = parser.parse_args()
    jobs = args.jobs
    command = args.command

    channels = [channel for channel in args.channel]
    packages = set(args.package_spec)
    if args.file is not None:
        name, channels_rc, packages_rc, pip = read_environment_description(args.file)
        channels.extend(channels_rc)
        packages |= set(packages_rc)
    else:
        name = args.name
        pip = []

    default_channels = _get_condarc_channels()
    channels.extend(default_channels)

    print("WARNING: mungo is still in alpha, use at your own risk.", file=sys.stderr)
    if command == "create":
        create_environment(name, channels, packages, pip, jobs)
    elif command == "install":
        install_packages(name, channels, packages, pip, jobs)
