
import sys
import argparse

from .submodules.ms_interface import MSFile
from .submodules.io import write_msconvert_config

def main():
    parser = argparse.ArgumentParser(description='A program to detect msconvert settings from a short mzML file.')
    parser.add_argument('-o', '--ofname', default='msconvert_params.txt', help='msconvert params file name')
    parser.add_argument('-f', '--format', choices=('stdout', 'file'), default='file',
                        help='Format to write msconvert config.')
    parser.add_argument('-t', '--demultiThreshold', default=0.45,
                        help='The max window overlap threshold at which the dmultiplex option will be set.')
    parser.add_argument('file')

    args = parser.parse_args()

    # detect isolation method
    ms_file = MSFile()
    ms_file.read(args.file)
    demultiplex = ms_file.calc_max_overlap() > args.demultiThreshold

    # write msconvert config
    if args.format == 'file':
        with open(args.ofname, 'w') as outF:
            write_msconvert_config(outF, demultiplex)
    else:
        write_msconvert_config(sys.stdout, demultiplex)
    

if __name__ == '__main__':
    main()

