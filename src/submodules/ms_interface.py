
from typing import Generator, Dict

from pyopenms import MzMLFile, MSExperiment

PAIR_ROUND = 2


def _round(n: float) -> float:
    return round(n, PAIR_ROUND)


class Pair:
    __slots__ = ('first', 'second')

    def __init__(self, first: float, second: float):
        self.first = _round(first)
        self.second = _round(second)
        if self.first > self.second:
            raise RuntimeError('Invalid mass window!')

    def dist(self) -> float:
        return self.second - self.first

    def overlap(self, rhs) -> float:
        ''' Calculate the overlap between 2 mass windows '''
        return max(0, min(self.second, rhs.second) - max(self.first, rhs.first))

    def __repr__(self):
        return f'Pair({self.first}, {self.second})'

    def __eq__(self, lhs):
        return self.first == lhs.first and self.second == lhs.second

    def __hash__(self):
        return hash((self.first, self.second))


class Scan:
    def __init__(self, data):
        self._data = data

    def _get_precursor(self):
        return self._data.getPrecursors()[0]

    def get_isolation_window(self) -> Pair:
        precursor = self._get_precursor()
        center = precursor.getPos()
        return Pair(center - precursor.getIsolationWindowLowerOffset(),
                    center + precursor.getIsolationWindowUpperOffset())

    def get_rt(self) -> float:
        return self._data.getRT()

    def get_ms_level(self) -> int:
        return self._data.getMSLevel()

    def get_length(self) -> int:
        return self._data.size()

    def get_min_max_mz(self) -> Pair:
        if not self._data.isSorted():
            self._data.sortByPosition()
        return Pair(self._data[0].getMZ(), self._data[self.get_length() - 1].getMZ())

class MSFile:
    def __init__(self):
        self.fname = None
        self._data = MSExperiment()

    def read(self, fname: str):
        self.fname = fname
        MzMLFile().load(self.fname, self._data)
        self._data.sortSpectra(True)

    def iter_spectra(self, min_level: int = 2, max_level: int = 2) -> Generator[Scan, None, None]:
        level_range = range(min_level, max_level + 1)
        for i in range(self._data.size()):
            if self._data.getSpectrum(i).getMSLevel() in level_range:
                yield Scan(self._data.getSpectrum(i))
    
    def get_ranges(self) -> Dict[str, float]:
        mz_ranges=dict()
        for i, s in enumerate(self.iter_spectra(min_level = 1)):
            if s.get_length() > 0:
                level = s.get_ms_level()
                min_max = s.get_min_max_mz()

                if level not in mz_ranges:
                    mz_ranges[level] = [min_max.first, 0]

                if min_max.first < mz_ranges[level][0]:
                    mz_ranges[level][0] = min_max.first
                if min_max.second > mz_ranges[level][1]:
                    mz_ranges[level][1] = min_max.second

        return mz_ranges


    def get_isolation_windows(self) -> Dict[Pair, float]:
        ret = dict()
        for s in self.iter_spectra():
            if s.get_isolation_window() not in ret:
                ret[s.get_isolation_window()] = s.get_rt()
        return ret

    def write_isolation_windows(self, fname: str):
        windows = self.get_isolation_windows()
        max_overlap = self.calc_max_overlap()
        with open(fname, 'w') as outF:
            outF.write('lo\thi\trt\n')
            for window, rt in self.windows.items():
                outF.write('{}\t{}\t{}\n'.format(window.first, window.second, rt))

    def calc_max_overlap(self, windows=None) -> bool:
        ''' Determine if the file contains overlapping isolation windows. '''

        # list of windows sorted by RT
        _windows = windows if windows is not None else self.get_isolation_windows()
        sorted_windows = [window for window, _ in sorted(_windows.items(), key = lambda x: x[1])]

        # find max overlap between all isolation windows
        max_overlap = 0
        for outer in sorted_windows:
            for inner in sorted_windows:
                if outer is not inner:
                    if outer == inner:
                        raise RuntimeError('Duplicate isolation windows!')
                    if ovl := outer.overlap(inner):
                        max_overlap = max(0, _round(ovl / outer.dist()))
        
        return max_overlap

