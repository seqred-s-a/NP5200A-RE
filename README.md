NP5200A Reverse Engineering
===========================

This is a reverse engineering project for the Moxa NP5200 series
serial device controllers. Currently, it includes the moxa_extractor script
which can unpack the contents of the .rom firmware update file.

Requirements
------------
* Python 3

Usage
-----
``` usage: moxa_extractor.py [-h] [-o OUTPUT_DIR] file

Unpack Moxa NP5200A firmware files

positional arguments:
  file                  File containing firmware image

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory for output
```

Ouptut
------
After running the script, output directory should contain a number of files
that were found in the table near the beginning of the firmware image. Those
will usually be related to NPort Web Console. In addition, all the data after
those files will be put in the firmware.bin file. It should contain ARM Cortex
A7 (little endian) machine code.