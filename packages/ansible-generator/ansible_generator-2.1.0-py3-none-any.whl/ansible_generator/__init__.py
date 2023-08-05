# -*- coding: utf-8 -*-
from ansible_generator.main import AnsibleGenerator
from argparse import ArgumentParser
from logging import DEBUG, INFO


def cli():
    parser = ArgumentParser(
        description="Generate an ansible playbook directory structure"
    )

    parser.add_argument(
        "-a", "--alternate-layout", action="store_true", dest="alternate_layout"
    )
    parser.add_argument(
        "-i",
        "--inventories",
        nargs="+",
        default=["production", "staging"],
        dest="inventories",
        type=str,
    )
    parser.add_argument("-r", "--roles", nargs="+", default=[], dest="roles", type=str)
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbosity")
    parser.add_argument(
        "-p", "--projects", nargs="+", default=[], dest="projects", type=str
    )

    args = parser.parse_args()

    if args.verbosity:
        verbosity = DEBUG
    else:
        verbosity = INFO

    generator = AnsibleGenerator(
        inventories=args.inventories,
        alternate_layout=args.alternate_layout,
        projects=args.projects,
        roles=args.roles,
        verbosity=verbosity,
    )
    generator.run()
