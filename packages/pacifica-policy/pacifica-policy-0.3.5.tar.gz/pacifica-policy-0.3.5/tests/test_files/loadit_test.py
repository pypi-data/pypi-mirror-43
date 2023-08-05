#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is used to generically load the test data."""
from os import getenv
from os.path import dirname, realpath, join
from json import loads
from pacifica.metadata.client import PMClient


def main():
    """Main method for loading the test data."""
    mdclient = PMClient(getenv('METADATA_URL', 'http://127.0.0.1:8121'))
    test_data_dir = dirname(realpath(__file__))
    object_order = [
        'users',
        'proposals',
        'instruments',
        'instrument_group',
        'proposal_instrument',
        'proposal_participant',
        'transactions',
        'transsip',
        'transaction_release'
    ]
    for obj in object_order:
        mdclient.create(obj, loads(
            open('{0}.json'.format(join(test_data_dir, obj))).read()))


if __name__ == '__main__':
    main()
