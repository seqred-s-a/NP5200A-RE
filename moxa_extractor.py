#!/usr/bin/env python3

import os
import argparse
import sys


p = argparse.ArgumentParser(description='Unpack Moxa NP5200A firmware files')
p.add_argument('file', type=str, help='File containing firmware image')
p.add_argument('-o', '--output-dir', type=str, help='Directory for output', default='out')
args = p.parse_args()

FILES_COUNT = 0x9a
FILE_TABLE  = 0x160

files = []
last_offset = 0

read_int = lambda x: int.from_bytes(x, signed=False, byteorder='little')

with open(args.file, 'rb') as f:
    # check for magic number at the beginning
    if f.read(4) != b'*FRM':
        print("Invalid format", file=sys.stderr)
        exit(-1)
    # find number of files (16-bit integer)
    f.seek(FILES_COUNT)
    count = read_int(f.read(2))
    f.seek(FILE_TABLE)
    for i in range(count):
        raw = f.read(0x40)
        tmp = {    'filename': raw[:0x30].replace(b'\x00', b''),
                   'unkn1'   : read_int(raw[0x30:0x34]),
                   'unkn2'   : read_int(raw[0x34:0x38]),
                   'size'    : read_int(raw[0x38:0x3b]),
                   'offset'  : (read_int(raw[0x3b:]) + 0x6000) >> 8}  # fixup offset
        files.append(tmp)

    try:
        os.mkdir('out')
    except FileExistsError:
        pass

    for entry in files:
        # keep the offset to ending of all files
        last_offset = max(last_offset, entry['size'] + entry['offset'])
        # extract each file
        f.seek(entry['offset'])
        with open(os.path.join(args.output-dir, entry['filename'].decode('ascii')), 'w+b') as outfile:
            outfile.write(f.read(entry['size']))

    # extract machine code
    with open(os.path.join(args.output-dir, 'firmware.bin'), 'w+b') as outfile:
        # files are padded so that they always start at multiples of 16
        f.seek(last_offset + 16 - (last_offset % 16))
        outfile.write(f.read())
