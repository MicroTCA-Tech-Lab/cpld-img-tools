#!/usr/bin/python3

###########################################################################
#      ____  _____________  __    __  __ _           _____ ___   _        #
#     / __ \/ ____/ ___/\ \/ /   |  \/  (_)__ _ _ __|_   _/ __| /_\  (R)  #
#    / / / / __/  \__ \  \  /    | |\/| | / _| '_/ _ \| || (__ / _ \      #
#   / /_/ / /___ ___/ /  / /     |_|  |_|_\__|_| \___/|_| \___/_/ \_\     #
#  /_____/_____//____/  /_/      T  E  C  H  N  O  L  O  G  Y   L A B     #
#                                                                         #
#          Copyright 2022 Deutsches Elektronen-Synchrotron DESY.          #
#                          All rights reserved.                           #
#                                                                         #
###########################################################################

import argparse
import os
from . import jed_conv
from bin2hpm import hpm_conv


def swap32(x):
    return int.from_bytes(x.to_bytes(4, "little"), "big")


def main():
    parser = argparse.ArgumentParser(description="CPLD .jed to HPM converter")
    parser.add_argument("infile", type=str, help="Source file for reading")
    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        help="output file (derived from input file if not set)",
    )
    parser.add_argument(
        "-b",
        "--binfile",
        action="store_true",
        help="also save intermediate binfile",
    )
    parser.add_argument(
        "-v",
        "--file-version",
        default="0.0",
        type=lambda x: [int(v, 10) for v in x.split(".")],
        help="file version information (format major.minor, e.g. 1.2)",
    )
    parser.add_argument(
        "-c", "--component", type=int, default=2, help="HPM component ID (default 2)"
    )
    parser.add_argument(
        "-m",
        "--manufacturer",
        type=lambda x: int(x, 16),
        default="00053f",
        help="IANA manufacturer ID (hex, 6 bytes max, default 53f)",
    )
    parser.add_argument(
        "-p",
        "--product",
        type=lambda x: int(x, 16),
        default="0000",
        help="IANA product ID (hex, 4 bytes max)",
    )
    parser.add_argument(
        "-i",
        "--img-hash",
        type=lambda x: int(x, 16),
        help="Image hash (e.g. Git commit, to override default hash)",
    )
    args = parser.parse_args()

    components = 1 << args.component
    v_maj = args.file_version[0]
    v_min = args.file_version[1]

    outfile = args.outfile
    if not outfile:
        basename, _ = os.path.splitext(os.path.basename(args.infile))
        outfile = basename + ".hpm"

    print(f"Parsing {args.infile} and creating binary update image")
    update_img, img_hash = jed_conv.jed_conv(args.infile, 512, args.img_hash)

    if args.binfile:
        basename, _ = os.path.splitext(os.path.basename(outfile))
        binfile = basename + ".bin"
        open(binfile, "wb").write(update_img)
        print(f"CPLD binfile {binfile} created.")

    print("Creating HPM image")
    hpm_img = hpm_conv.hpm_conv(
        update_img,
        False,
        manufacturer_id=args.manufacturer,
        product_id=args.product,
        components=components,
        version_major=v_maj,
        version_minor=v_min,
        version_aux=swap32(img_hash),
        desc_str=os.path.basename(args.infile)[:20],
    )

    # Write HPM file
    with open(outfile, "wb") as f:
        f.write(hpm_img)

    print(f"CPLD file {outfile} created. Config hash: {img_hash:08X}")


if __name__ == "__main__":
    main()
