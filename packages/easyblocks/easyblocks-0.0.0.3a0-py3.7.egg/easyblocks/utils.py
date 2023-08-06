#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def to_bytes(value):
    if type(value) == int:
        return int_to_bytes(value)
    elif type(value) == str:
        return str_to_bytes(value)
    elif type(value) == dict:
        return str_to_bytes(dump_dict(value))
    raise ValueError

def str_to_bytes(string):
    return bytes(string, 'utf-8')

def bytes_to_str(bytes_string):
    return bytes_string.decode('utf-8')

def bytes_to_int(bytes_string):
    return int(bytes_to_str(bytes_string))

def int_to_bytes(integer):
    return str_to_bytes(str(integer))

def dump_dict(dict):
    return json.dumps(dict, separators=(',', ':'), ensure_ascii=False)