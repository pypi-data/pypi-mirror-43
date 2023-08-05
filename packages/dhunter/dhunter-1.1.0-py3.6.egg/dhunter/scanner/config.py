# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import os
from argparse import Namespace

from ..core.config_base import ConfigBase
from ..util.overrides_decorator import overrides


class Config(ConfigBase):

    @staticmethod
    @overrides(ConfigBase)
    def from_args(args: Namespace) -> 'Config':
        from ..core.log import Log
        from ..util.util import Util

        config = Config()

        _keys = [
            'src_dirs',
            'db_file',
            'min_size',
            'max_size',
            'force_rehash',
            'verbose',
            'debug',
            'debug_verbose',
            'dont_save_dot_file',
        ]
        for key in _keys:
            config.__setattr__(key, getattr(args, key))

        # noinspection PyUnresolvedReferences
        config.min_size = 0 if config.min_size is None else Util.size_to_int(str(config.min_size[0]))
        # noinspection PyUnresolvedReferences
        config.max_size = 0 if config.max_size is None else Util.size_to_int(str(config.max_size[0]))

        config.db_file = None if config.db_file is None else config.db_file[0]
        if config.db_file is not None and os.path.exists(config.db_file):
            Log.abort('Project file already exists.')

        # Let's check if all paths to scan are in fact valid and existing folders
        for single_dir in config.src_dirs:
            if not os.path.exists(single_dir):
                Log.abort('Folder "{dir}" does not exists'.format(dir=single_dir))
            elif not os.path.isdir(os.path.abspath(single_dir)):
                Log.abort('Path "{dir}" is not a folder'.format(dir=single_dir))

        if config.dont_save_dot_file and config.db_file is None:
            Log.abort('When using --read-only flag you must create database file with --db, otherwise '
                      'the whole scanning process makes no much sense.')

        # after that point, data in Config should be sanitized, validated, usable and useful

        from ..core.filter import Filter
        config.filter = Filter(config)

        return config
