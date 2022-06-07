
import argparse

from submodules.ms_interface import MSFile

def main():
    parser = argparse.ArgumentParser(description='A program to detect msconvert settings from a short mzML file.')
    parser.add_argument('file')

    args = parser.parse_args()

    ms_file = MSFile()
    ms_file.read(args.file)
    for ovl in ms_file.overlapping:
        print(ovl)


if __name__ == '__main__':
    main()

