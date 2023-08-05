#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~ Jesse K. Rubin ~ Pretty Useful Python

from __future__ import print_function
from __future__ import with_statement

from codecs import getwriter
from datetime import datetime
from io import open
from itertools import count
from sys import stderr
from time import sleep

try:
    from ujson import dump
    from ujson import load
except:
    from json import dump
    from json import load
from os import path
from os import remove
from msgpack import pack
from msgpack import unpack


def timestamp():
    """Time stamp string w/ format yyyy-mm-ddTHH-MM-SS

    :return: timestamp string
    """
    """Time stamp string w/ format yyyy-mm-ddTHH-MM-SS"""
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")


def safe_path(filepath):
    """

    :param filepath: 

    """
    if path.exists(filepath):
        f_bn, f_ext = path.splitext(filepath)
        for n in count(1):
            safe_save_path = f_bn + "_({}).".format(str(n)) + f_ext
            if not path.exists(safe_save_path):
                return safe_save_path
    return filepath


def ensure_save(filepath, n=0):
    try:
        assert path.exists(filepath)
        return True
    except AssertionError:
        sleep(1)
        if n > 5:
            return False
        return ensure_save(filepath, n + 1)


def savings(filepath, string, clobber=True):
    """Save s(tring) to filepath as txt file

    :param filepath: Filepath save location
    :param string: File as a string to be saved
    :param clobber: Save over a file if the filepath exists
    :return: None? what do you want? confirmation?

    """
    if not clobber and path.exists(filepath):
        filepath = safe_path(filepath)
    elif path.exists(filepath):
        remove(filepath)
    try:
        with open(safe_path(filepath) if clobber else filepath, "wb") as file:
            file.write(string.encode("utf-8"))
    except Exception as e:
        raise e


def loads(filepath):
    """Load a (txt) file as a string

    :param filepath: return:

    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError as e:
        with open(filepath, "r", encoding="latin2") as f:
            return f.read()


def sjson(filepath, data, min=False):
    """Save json-serial-ize-able data to a specific filepath.

    :param filepath: save filepath
    :param data: json ready data
    :param min: minified format flag
    :return: None
    """
    if type(data) == dict and any(type(val) == bytes for val in data.values()):
        data = {k: str(v, encoding="utf-8") for k, v in data.items()}
    with open(filepath, "wb") as jsonfile:
        if min:
            dump(data, getwriter("utf-8")(jsonfile), ensure_ascii=False)
        else:
            dump(
                data,
                getwriter("utf-8")(jsonfile),
                indent=4,
                sort_keys=True,
                ensure_ascii=False,
            )


def save_jasm(filepath, data, min=False):
    """Alias for sjson (which stands for 'save-json')"""
    return sjson(filepath, data, min)


def sjasm(filepath, data, min=False):
    """Alias for sjson (which stands for 'save-json')"""
    return sjson(filepath, data, min)


def ljson(filepath):
    """Load a json file given a filepath and return the file-data

    :param filepath: path to the jasm file you want to load
    :return: Loaded file contents
    """

    with open(filepath) as infile:
        return load(infile)


def load_jasm(filepath):
    """Alias for ljson (which stands for 'load-json')"""
    return ljson(filepath)


def ljasm(filepath):
    """Alias for ljson (which stands for 'load-json')"""
    return ljson(filepath)


def spak(filepath, data):
    with open(filepath, "wb") as pakfile:
        pack(data, pakfile)


def lpak(filepath):
    with open(filepath, "rb") as pakfile:
        return unpack(pakfile, raw=False)


if __name__ == "__main__":
    pass
