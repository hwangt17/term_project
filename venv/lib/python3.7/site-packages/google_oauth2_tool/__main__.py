#!/user/bin/env python
"""
This utility helps create OAuth2 key file from OAuth2 client id file

(c) dlancer, 2019

"""

import argparse
import sys
import json

from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--scope', required=True, default=None, help='path to file with required google api scopes')
    parser.add_argument('--source', required=True, default=None, help='path to source oath2 client id file')
    parser.add_argument('--destination', required=True, default=None, help='path to destination oath2 client key file')
    parser.add_argument('--strip', type=str2bool, nargs='?', const=True, default='no',
                        help='strip key file as string for ENV var')
    flags = parser.parse_args()

    try:
        infile = open(flags.scope)
        scopes = infile.readlines()
        scopes = [scope.strip(' \r\n') for scope in scopes]
    except IOError:
        sys.exit('file with required scopes missed')

    flow = flow_from_clientsecrets(flags.source, scope=scopes)
    storage = Storage(flags.destination)
    tools.run_flow(flow, storage, flags)

    if flags.strip:
        with open(flags.destination, 'r') as infile:
            content = json.load(infile)
        with open(flags.destination, 'w') as outfile:
            json.dump(content, outfile, separators=(',', ':'))


if __name__ == '__main__':
    main()
