# Series Organizer
Meant for organizing tv show files for use with XBMC.

## Arguments
- scandir
  - Directory to scan for media. The directory is scanned recursively so it is OK to have nested directories.
  - Defaults to .
- title
  - The title of the show.
  - Ex: "Archer (2009)".
  - Used when creating the output directory
- output_root
  - Where to copy output to. When the script finishes this output_root will contain a folder named <Title> for whatever title you supplied. Within that <Title> folder there will be a folder for each Season. Within each season folder will be each episode in the format s<season_number>e<episode_number>.<file_extension>
  - Ex: /home/<you>/Videos
- dry-run
  - No files are copied and no directories are created, useful for testing regexes.
- season_regex
  - regex used for extracting the season number from a filename.
- episode_regex
  - Same as above but for episodes.
- extension_regex
  - same as above but for the extension.

## How it works

The script walks over all files in scandir recursively. For each file found:

1. Attempt to extract the season number, episode number, and file extension using the supplied regexes. If any of those fields are not found, the file is skipped.
2. With the supplied output root, series title and the parsed season number the script will check if the directory <output root>/<series title>/Season <season number> exists and create it if not.
3. The script will then copy the file to that directory with the format s<season number>e<episode number>.<extension>
