# SignalDesktopParser

A python parser to parse the forensic info from MacOSX Signal Database.

Location of Signal Database in MacOSX: `/Users/<myusername>/library/Application Support/discord`

**Note:**
- This script works only on the decrypted MacOS Signal database.

## Requirements

Python 3.9 or above. The older versions of Python 3.x should work fine as well.

## Dependencies

These are the required libraries needed to run this script.

argparse
csv
os
sqlite3

## Usage

This is a CLI based tool.

```bash
$ python SignalDesktopParser.py -f <path to decrypted Signal Database>
```

To view the help:

```bash
$ python .\SignalDesktopParser.py -h
```

![](https://i.imgur.com/smZuJ8G.png)

## Author 👥

B. Krishna Sai Nihith
+ Twitter: [@_Nihith](https://twitter.com/_Nihith)
+ Personal Blog: https://g4rud4.gitlab.io