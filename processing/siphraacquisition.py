import pandas as pd
from typing import TypeVar
from pathlib import Path

PathLike = TypeVar("PathLike", str, Path, None)

class SiphraAcquisition:
    '''
    Class to store information about SIPHRA acquisitions and load data efficiently.
    '''

    ch_strs = [f"Ch{_}" for _ in range(17)] # Names of the channels in the dataframe.

    def __init__(self, filepath: PathLike,
                 active_chs:int | list[int],
                 exposure_sec:float,
                 sipm_chs:str | None = None, ):

        self.filepath = self._resolve_path(filepath)
        self.active_chs = self._resolve_active_chs(active_chs)
        self.exposure = exposure_sec
        self.sipm_chs = sipm_chs


    def _resolve_path(self, f):
        try:
            f = Path(f).resolve()
            if not f.exists():
                raise FileNotFoundError(f"File {f} does not exist")
            if not f.suffix in ['.csv', '.pkl']:
                raise NotImplementedError("Path does not point to a .csv or a .pkl file")
            return f
        except Exception as e:
            raise ValueError(f"Invalid filepath argument: {e}")

    def _resolve_active_chs(self, chs) -> list[int]:
        channels = [chs] if isinstance(chs, int) else chs
        if all(isinstance(_, int) and 1 <= _ <= 16 for _ in channels):
            return channels
        else:
            raise ValueError("Channels outside the allowed range (1 - 16)")

    def _read_column(self, col_name: str) -> numpy.ndarray:
        try:
            if self.filepath.suffix == '.csv':
                return pd.read_csv(self.filepath, usecols=[col_name])[col_name].to_numpy()

            elif self.filepath.suffix == '.pkl':
                df = pd.read_pickle(self.filepath)
                data = df[col_name].to_numpy()
                del df
                return data
        except Exception as e:
            raise ValueError(f"Cannot retrieve data from field {col_name} in file {self.filepath.name}: {e}")

    # def _get_ch_data(self, ch: int) -> np.ndarray:
    #     return self._read_column(self.ch_strs[ch])

    def _get_active_chs_data(self):
        '''
        Returns a dict whose keys are the channel numbers and whose values are
        numpy.ndarrays containig the corresponding acquisition data of that channel.
        '''
        # if len(self.active_chs) == 1:
        #     return self._read_column(self.ch_strs(self.active_chs[0]))
        active_chs_data = {}
        for ch in self.active_chs:
             active_chs_data[ch] = self._read_column(self.ch_strs[ch])
        return active_chs_data

    def __getitem__(self, items):
        if any(items == _ for _ in ('active', 'a', 'A')):
            return self._get_active_chs_data()

        elif any(items == _ for _ in ('s', '+', 'S')):
            return self._read_column('Summed')

        elif isinstance(items, (int, str)):
            col_name = self.ch_strs[items] if isinstance(items, int) else items
            return self._read_column(col_name)

        elif isinstance(items, list) and all(isinstance(item, int) for item in items):
            data = {}
            for ch in items:
                data[ch] = self._read_column(self.ch_strs[ch])
            return data

        elif isinstance(items, list) and all(isinstance(item, (int, str)) for item in items):
            data = {}
            for item in items:
                col_name = self.ch_strs[item] if isinstance(item, int) else item
                data[col_name] = self._read_column(col_name)
            return data

    def as_dataset(self):
        file_type = self.filepath.suffix
        if file_type == ".csv":
            return pd.read_csv(self.filepath)
        elif file_type == ".pkl":
            return pd.read_pickle(self.filepath)



