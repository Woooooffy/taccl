#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from taccl.cli import *
from gurobipy import Env
import argparse
import argcomplete
import sys
import os

def main():
    parser = argparse.ArgumentParser('taccl')

    cmd_parsers = parser.add_subparsers(title='command', dest='command')
    cmd_parsers.required = True
    conn_params = {
            "WLSACCESSID": os.environ["GUROBI_WLSACCESSID"],
            "WLSSECRET": os.environ["GUROBI_WLSSECRET"],
            "LICENSEID": int(os.environ["GUROBI_LICENSEID"]),
    }
    env = Env(params=conn_params)
 

    handlers = []
    handlers.append(make_handle_solve_comm_sketch(cmd_parsers))
    handlers.append(make_handle_combine_comm_sketch(cmd_parsers))
    handlers.append(make_handle_ncclize(cmd_parsers))

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    
    for handler in handlers:
        if handler(args, args.command, env):
            break
    env.dispose()

if __name__ == '__main__':
    main()
