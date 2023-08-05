dhunter
=======
 dhunter (pronounced The Hunter) is [d]uplicate [hunter] utility, designed
 to help scanning and processing large sets of files. Uses content based
 file duplicates matching and smart caching for faster directory scanning,
 data changes detection and processing.

Features
========
 * Content based file matching
 * Designed to work with lot of data:
   * caches folder scaning results for quick reuse
   * directory scanning can be aborted and **resumed** at any moment
 * Smart content filters:
   * Ignores zero length files
   * Ignores folders like `.git`, `.cvs`, `.svn`
   * Supports user configurable file size filter (min and/or max)

Requirements
============
 Requires Python 3.6 or newer.

Installation
============
 Use `pip` package manager to install `dhunter` on your machine:
 
    pip install dhunter

 If you want it install for current user only add `--user` flag to above.

 Once installed you should have `dscan` and `dhunt` available.

Usage
=====
 See detailed [usage examples](docs/usage.md).


Credits and license
===================
 * Written and copyrighted ©2018-2019 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
 * dhunter is open-sourced software licensed under the MIT license
