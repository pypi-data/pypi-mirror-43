# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

from abc import abstractmethod
from argparse import Namespace
from typing import List


class ConfigBase(object):

    def __init__(self):
        self.src_dirs: List[str] = []
        self.db_file: str or None = None
        self.sort_by: str = None
        self.reverse_order: bool = False
        self.limit: int = 0
        self.min_size: int = 1024
        self.max_size: int = 0
        self.force_rehash: bool = False
        self.verbose: bool = False
        self.debug: bool = False
        self.debug_verbose: bool = False
        self.filter = None
        self.dont_save_dot_file = False

    @staticmethod
    @abstractmethod
    def from_args(args: Namespace) -> 'ConfigBase':
        raise NotImplementedError
