#!/usr/bin/env python3
"""
Determine the approriate destination for a completed transmission torrent download.

See the [[file:~/.dotfiles/programs/transmission/README.org][README]].
"""

import os
import sys
import json
import logging
import pathlib as p

from watch_config import WatchConfig

def Path(path):
    return p.Path(path).expanduser()

def relative_p(path, parent):
    # TODO switch to optimised
    return parent in path.parents

def normal_download_directory(location, incomplete):
    if not incomplete:
        logging.warning('no incomplete downloads directory supplied')
        # don't know where you normally download to, so not normal dir
        return False

    return relative_p(location, incomplete)

def check_watch_hirearchy(torrent: p.Path, config) -> str:
    """check a users watch directory configuration to determine where a
    torrent should be placed.

    For example, if a user is watching `~/torrents' and the current torrent
    is placed in `~/torrents/foo/bar/' then return `foo/bar'.

    Parameters
    ----------
    torrent
        path to the torrent from which we've been downloading
    config
        path to users watcher configuration, see ./watcher
    """
    if not config:
        logging.warning('no watcher config supplied, skipping watch check')
        return None

    if not torrent:
        logging.warning('no torrent file supplied, skipping watch check')
        return None

    if not isinstance(config, WatchConfig):
        with config as fd:
            config = WatchConfig(json.load(fd))

    for watch_dir in (config.added / x['directory'] for x in config.rules):
        if watch_dir.exists() and relative_p(torrent, watch_dir):
            return torrent.parent.relative_to(watch_dir)

def check_incomplete_hirearchy(location: p.Path, incomplete: p.Path) -> str:
    """check the current location (where it was downloaded) to determine
    where a torrent should be placed.

    For example, if torrents are normally downloaded to `~/getting' but the
    current location is actually in `~/getting/foo/bar' then return foo/bar.

    Parameters
    ----------
    location
        the full path to where the torrent was downloaded.
    incomplete
        where in progress (downloading) torrents are placed.
    """
    if relative_p(location, incomplete):
        relative = location.parent.relative_to(incomplete)
        if str(relative) != '.': return relative

def check_hirearchy(args):
    return \
        check_incomplete_hirearchy(args.location, args.incomplete) or \
        check_watch_hirearchy(args.torrent, args.watch)

def get_dest_directory(args):
    """determine where a torrent should be placed."""
    dest = args.default
    if not dest:
        logging.warning('no default destination supplied')

    if normal_download_directory(args.location, args.incomplete):
        if not args.downloads:
            logging.warning('no downloads root supplied, ignoring structure checks')
        else:
            hirearchy = check_hirearchy(args)
            if hirearchy and str(hirearchy) != '.':
                dest = args.downloads / hirearchy
    else:
        dest = None  # keep download in it's current, non-normal, location

    return dest

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='tranmission id for torrent')
    parser.add_argument('torrent', type=Path, help='path to torrent file')
    parser.add_argument('location', type=Path, help='current location of download')

    config_group = parser.add_argument_group('config')
    config_group.add_argument('-r', '--downloads', metavar='DIR', type=Path,
                              help='root directory for downloads')
    config_group.add_argument('-d', '--default', metavar='DIR', type=Path,
                              help='default directory to put complete downloads')
    config_group.add_argument('-i', '--incomplete', metavar='DIR', type=Path,
                              help='directory where incomplete downloads are placed')
    config_group.add_argument('-w', '--watch', metavar='FILE',
                              type=argparse.FileType('r', encoding='utf8'),
                              help='path to default watcher config file')

    log_group = parser.add_argument_group('logging')
    log_group.add_argument('-l', '--log-level', type=lambda x: getattr(logging, x.upper()),
                           metavar='LEVEL', default=logging.INFO,
                           help='verbosity of logging output')
    log_group.add_argument('-L', '--log-file', metavar='FILE', default=sys.stderr,
                           type=argparse.FileType('a', encoding='utf8'),
                           help='file to write logging output to')

    args  = parser.parse_args()
    vargs = vars(args)

    logging.basicConfig(
        level=vargs.pop('log_level'),
        stream=vargs.pop('log_file'))

    dest = get_dest_directory(args)
    if dest: print(str(dest))
