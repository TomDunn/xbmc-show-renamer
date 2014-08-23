#!/usr/bin/env python2.7

from argparse import ArgumentParser
import os
import re
import shutil

def get_match_or_none(regex, string):
    match = re.search(regex, string)

    if match is None:
        return None

    return match.group(0)

parser = ArgumentParser(description="Copy TV series to XBMC compatible dest")

parser.add_argument('--output_root',
        action='store',
        default='~/Videos/',
        dest='output_root',
        help="Where output will be copied to",
        type=str)

parser.add_argument('--scandir',
        action='store',
        default='.',
        dest='scandir',
        help="Directory to scan for videos",
        type=str)

parser.add_argument('--title',
        action='store',
        dest='feature_title',
        help="The series title is required. Ex: Archer (2009)",
        required=True,
        type=str)

parser.add_argument('--season_regex',
        action='store',
        dest='season_regex',
        default='^[0-9]?[0-9](?=\.)',
        help="Regex used for extracting season number from filenames",
        type=str)

parser.add_argument('--episode_regex',
        action='store',
        dest='episode_regex',
        default='(?<=\.)[0-9]?[0-9]',
        help="Regex used for extracting episode number from filenames",
        type=str)

parser.add_argument('--extension_regex',
        action='store',
        dest='extension_regex',
        default='(?<=\.)[a-z][a-z][a-z|1-9]$',
        help="Regex used for extracting file extension",
        type=str)

parser.add_argument('--dry_run',
        action='store_true',
        default=False,
        dest='dry_run',
        help='If true, program copies nothing. Useful for verifying regexes')

arguments = parser.parse_args()
file_name_template  = "s%se%s.%s" # ex: s01e01.mp4
print arguments

for root, dirs, filenames in os.walk(arguments.scandir):
    for filename in filenames:

        # extract season, episode and file extension from filename
        season  = get_match_or_none(arguments.season_regex, filename)
        episode = get_match_or_none(arguments.episode_regex, filename)
        exten   = get_match_or_none(arguments.extension_regex, filename)

        # skip any files that don't match
        if season is None or episode is None or exten is None:
            print "Skipping: ", filename
            continue

        new_filename  = file_name_template % (season, episode, exten)
        season_title  = "Season %s" % season

        new_file_path = os.path.join(arguments.output_root,
            arguments.feature_title,
            season_title)

        print "Copying: %s -> %s" % (os.path.join(arguments.scandir, root, filename), os.path.join(new_file_path, new_filename))

        if not os.path.exists(new_file_path) and not arguments.dry_run:
            os.makedirs(new_file_path)

        if not arguments.dry_run:
            shutil.copy2(os.path.join(root, filename), os.path.join(new_file_path, new_filename))
