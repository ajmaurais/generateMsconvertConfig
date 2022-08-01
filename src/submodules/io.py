
import sys
import json
from math import floor, ceil

DEFAULT_PARAMS = [('mzML', True),
                  ('mz64', True),
                  ('inten64', True),
                  ('simAsSpectra', True),
                  ('filter', 'peakPicking vendor msLevel=1-2')]
DEMULTIPLEX = ('filter', 'demultiplex optimization=overlap_only massError=10.0ppm')

def write_msconvert_config(out, demultiplex: bool):
    options = DEFAULT_PARAMS
    if demultiplex:
        options.append(DEMULTIPLEX)
    
    for option in options:
        if isinstance(option[1], bool):
            v=str(option[1]).lower()
        elif isinstance(option[1], str):
            v=f'"{option[1]}"'
        else:
            v=option[1]
        out.write(f'{option[0]}={v}\n')


def write_file_ranges(ranges, range_format, round_mz=True):
    round_functions = [floor, ceil]

    if range_format == 'txt':
        for level, r in sorted(ranges.items()):
            for i, v in enumerate(('min', 'max')):
                mz = round_functions[i](r[i]) if round_mz else r[i]
                sys.stdout.write(f'level {level} {v}: {mz}\n')

    elif range_format == 'json':
        d = {'levels': dict()}
        for level, r in sorted(ranges.items()):
            d['levels'][level] = {'min': r[0], 'max': r[1]}
        json.dump(d, sys.stdout, indent = 4)
        sys.stdout.write('\n')

             

