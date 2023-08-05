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
        group.add_argument(metavar='FILE', action='store', dest='db_file', nargs=1,
                           help='Name of project file to process.')

        group = parser.add_argument_group('Sorting and results limit')
        group.add_argument('-s', '-sort', '--sort',
                           metavar='MODE', action='store', dest='sort_by', nargs=1,
                           help='Results sorting order. Allowed modes are: ' + ', '.join(Const.ALLOWED_SORT_VALUES))
        group.add_argument('-r', '-reverse', '--reverse',
                           action='store_true', dest='reverse_order',
                           help='Reverses order of displayed data.')
        group.add_argument('-l', '-limit', '--limit',
                           metavar='COUNT', action='store', dest='limit', nargs=1, type=int,
                           help='Limit number of shown results to given count. '
                                'Default is 0, which means no limits.')

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
