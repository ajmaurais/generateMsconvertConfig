
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



