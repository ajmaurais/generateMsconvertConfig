
import sys
import argparse

from .submodules.ms_interface import MSFile
from .submodules.io import write_file_ranges

def main():
    parser = argparse.ArgumentParser(description='Get charge and mz ranges for a mzML file.')
    parser.add_argument('-f', '--format', choices=('json', 'txt'), default='txt',
                        help='The format to write data to.')
    parser.add_argument('file', help='A mzML file to read from.')

    args = parser.parse_args()
    
    # read file and determine ranges
    ms_file = MSFile()
    ms_file.read(args.file)
    ranges = ms_file.get_ranges()
    
    write_file_ranges(ranges, args.format)

if __name__ == '__main__':
    main()


