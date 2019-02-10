# -*- coding: utf-8 -*-

import json

import attrdict


def load_config(filename_config):

    with open(filename_config, str("r")) as finp:
        config = json.load(finp)

    return attrdict.AttrDict(config)
