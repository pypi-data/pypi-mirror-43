# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import argparse

from ..core.args_base import ArgsBase
from ..core.const import Const


class Args(ArgsBase):
    """Handles command line arguments"""

    # noinspection PyTypeChecker
    def parse_args(self) -> argparse.Namespace:
        """Parses command line arguments
        """
        parser = self._get_parser()

        group = parser.add_argument_group('Project')
        group.add_argument('-db', '--db',
                           metavar='FILE', action='store', dest='db_file', nargs=1,
                           help='Name of project file to create.')

        group.add_argument(
                metavar='DIR', action='store', dest='src_dirs', nargs='+',
                help='Directories to scan and include in the project file.')

        group = parser.add_argument_group('Misc')
        group.add_argument('-r', '-rehash', '--rehash',
                           action='store_true', dest='force_rehash',
                           help='Ignores existing file hash cache files ({dot}) and regenerates '
                                'all the hashes.'.format(dot=Const.FILE_DOT_DHUNTER))
        group.add_argument('-ro', '--ro', '--read-only',
                           action='store_true', dest='dont_save_dot_file',
                           help='Tells the scanner to treat all the folders as read only and do not '
                                'write cache file ({dot})'.format(dot=Const.FILE_DOT_DHUNTER)
                           )

        self._add_filter_option_group(parser)

        self._add_other_option_group(parser)

        # this trick is to enforce stacktrace in case parse_args() fail (which should normally not happen)
        # old_config_debug = config.debug
        # if not config.debug:
        #     config.debug = True

        args = parser.parse_args()

        # config.debug = old_config_debug

        # we need at least one command set
        # if args.save_state is None and args.load_state is None and args.src_dirs is None:
        #     Log.abort('No action specified')

        self._debug_check(args)

        return args
