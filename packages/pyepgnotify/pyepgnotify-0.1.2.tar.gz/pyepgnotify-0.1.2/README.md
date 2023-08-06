# pyepgnotify
Reads EPG data from VDR, checks against a list of desired program titles, subtitles, or descriptions, and sends found programs via mail or it to stdout.

# Usage
```
usage: pyegnotify [-h] [--config file] [--stdout] [--cache-file file] 
                  [--epg-dst-file file]

Parses EPG data from VDR, checks against search config and sends mail. Already
sent programs are stored in a cache to avoid multiple notifications on same
program.

optional arguments:
  -h, --help           show this help message and exit
  --config file        Config file. If not given ~/epgnotify.yml is used.
  --stdout             Additionally print result to stdout
  --cache-file file    Optionally, cache file location, default
                       epgnotfiy.cache.yaml in home directory is used
  --epg-dst-file file  Store received EPG data to a file
```
