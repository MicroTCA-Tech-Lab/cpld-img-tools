# cpld_img_tools

This is a set of tools to convert `.jed` fuse files for Lattice CPLDs into binary files that the [DMMC-STAMP](https://techlab.desy.de/products/desy_mmc_solution/desy_mmc_stamp/index_eng.html) can use for in-application update of a CPLD.

## `jed_conv`

This is a tool to convert a `.jed` fuse file into a binary format e.g. for embedding in the MMC firmware image as used in the [DMMC-STAMP SDK](https://techlab.desy.de/products/desy_mmc_solution/desy_mmc_software_development_kit/index_eng.html).

### Usage

```
$ jed_conv --help
usage: jed_conv [-h] [-o OUTFILE] [-b BLKSIZE] infile

.jed file parser / converter

positional arguments:
  infile                Source file for reading

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file (derived from input file if not set)
  -b BLKSIZE, --blksize BLKSIZE
                        max. block size per packet
```

## `cpld2hpm`

This is a tool to convert a `.jed` fuse file into a HPM upgrade file that can be used to update a CPLD on the AMC payload, e.g. on the [DAMC-FMC1Z7IO](https://techlab.desy.de/products/amc/damc_fmc1z7io/index_eng.html).

See [bin2hpm](https://github.com/MicroTCA-Tech-Lab/bin2hpm) for HPM details.

### Usage

```
cpld2hpm --help
usage: cpld2hpm [-h] [-o OUTFILE] [-v FILE_VERSION] [-c COMPONENT] [-m MANUFACTURER] [-p PRODUCT] infile

CPLD .jed to HPM converter

positional arguments:
  infile                Source file for reading

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file (derived from input file if not set)
  -v FILE_VERSION, --file-version FILE_VERSION
                        file version information (format major.minor, e.g. 1.2)
  -c COMPONENT, --component COMPONENT
                        HPM component ID (default 2)
  -m MANUFACTURER, --manufacturer MANUFACTURER
                        IANA manufacturer ID (hex, 6 bytes max, default 53f)
  -p PRODUCT, --product PRODUCT
                        IANA product ID (hex, 4 bytes max)
```
