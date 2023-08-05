# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import datetime
import os
import tempfile

from .args import Args
from .config import Config
from ..core.config_base import ConfigBase
from ..core.const import Const
from ..core.hash_manager import HashManager
from ..core.log import Log
from ..util.util import Util


# noinspection PyMethodMayBeStatic
class Hunter(object):
    _instance: 'Hunter' or None = None

    def __init__(self):
        self.config: ConfigBase or None = None

    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_instance() -> 'Hunter':
        if Hunter._instance is None:
            Hunter._instance = Hunter()
        return Hunter._instance

    # ------------------------------------------------------------------------------------------------------------

    @property
    def config(self) -> ConfigBase:
        return self._config

    @config.setter
    def config(self, val: ConfigBase) -> None:
        self._config = val

    # ------------------------------------------------------------------------------------------------------------

    def generate_db_file_name(self) -> str:
        idx = None
        while True:
            suffix = '' if idx is None else '_{idx}'.format(idx=idx)
            db_file = os.path.join(tempfile.gettempdir(), '{app}_{stamp}{suffix}.sqlite'.format(
                    app=Const.APP_NAME, stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), suffix=suffix))
            if not os.path.exists(db_file):
                break

            idx += 1
            continue

        return db_file

    # ------------------------------------------------------------------------------------------------------------

    def show_stats(self) -> None:
        hm = HashManager.get_instance()

        dir_cnt, file_cnt, total_file_size = hm.get_stats()
        Log.banner([
            'Dirs : {}'.format(dir_cnt),
            'Files: {}'.format(file_cnt),
            'Size : {}'.format(Util.size_to_str(total_file_size))
        ])

    # ------------------------------------------------------------------------------------------------------------

    def show_duplicates(self, limit: int = 0, sort_by: str = 'size', reverse_order: bool = False) -> None:
        hm = HashManager.get_instance()

        # get all files with non unique hashes (at least 2 counts)
        dupli_hashes = hm.get_hashes_by_count_threshold(2, limit, sort_by, reverse_order)

        if not dupli_hashes:
            Log.i('No duplicated files found.')
            return

        Log.banner('Duplicates')

        stats_duplicates_total_count = 0
        stats_duplicates_bytes_total = 0

        cursor = hm.db.cursor()
        query = 'SELECT * FROM `files` WHERE `hash` = ? ORDER BY `path`,`name` '
        for file_hash_idx, file_hash in enumerate(dupli_hashes, start=1):
            cursor.execute(query, (file_hash,))

            group_header_shown = False
            dupli_rows = cursor.fetchall()
            for idx, row in enumerate(dupli_rows, start=1):
                if not group_header_shown:
                    duplicate_count = (len(dupli_rows) - 1)
                    total_duplicates_size = duplicate_count * row['size']

                    stats_duplicates_total_count += duplicate_count
                    stats_duplicates_bytes_total += total_duplicates_size

                    Log.level_push('{idx:2d}: size: {size:s}, duplicates: {dupes:d}, wasted: {wasted:s}'.format(
                            idx=file_hash_idx, size=Util.size_to_str(row['size']),
                            dupes=duplicate_count, wasted=Util.size_to_str(total_duplicates_size)),
                    )
                    group_header_shown = True

                Log.i('{idx:2d}: {path}'.format(idx=idx, path=os.path.join(row['path'], row['name'])))

            Log.level_pop()

        Log.level_push('Summary')
        fmt = '{files_cnt:d} files has {dupes_cnt:d} duplicates, wasting {size:s}.'
        Log.i(fmt.format(files_cnt=len(dupli_hashes), dupes_cnt=stats_duplicates_total_count,
                         size=Util.size_to_str(stats_duplicates_bytes_total)))
        Log.level_pop()

    # ------------------------------------------------------------------------------------------------------------

    def main(self) -> int:
        rc = 0

        try:
            # parse common line arguments
            args = Args()

            self.config = Config.from_args(args.parse_args())
            Log.configure(self.config)
            Log.disable_buffer()

            # init hash manager singleton
            HashManager.get_instance(self.config.db_file, self.config)

            # if self.config.duplicates:
            self.show_duplicates(self.config.limit, self.config.sort_by, self.config.reverse_order)
            # elif self.config.cmd_stats:
            #     self.show_stats()

        except (ValueError, IOError) as ex:
            if not self.config.debug:
                raise
            Log.e(str(ex))
            rc = 1

        return rc

    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def start() -> int:
        """Application entry point.
        """
        Util.validate_env()

        app = Hunter()
        return app.main()
