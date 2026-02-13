import ROOT
import numpy as np
import pandas as pd
from collections import UserDict
from typing import TypeVar
from pathlib import Path
import os

PathLike = TypeVar("PathLike", str, Path, None)

class ChDataDict(UserDict):
    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError("Key must be an integer")
        if not isinstance(value, np.ndarray):
            raise TypeError("Value must be a numpy array")
        super().__setitem__(key, value)

class SiphraAcquisition:
    '''
    Class to store information about SIPHRA acquisitions and load data efficiently.
    '''

    ch_strs = [f"Ch{_}" for _ in range(17)]

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
            raise ValueError("active_chs should be an int or list of integers between 1 and 16")

    def read_column(self, col_name: str) -> np.ndarray:
        try:
            if self.filepath.suffix == '.csv':
                return pd.read_csv(self.filepath, usecols=[col_name])[col_name].to_numpy()

            elif self.filepath.suffix == '.pkl':
                df = pd.read_pickle(self.filepath)
                data = df[col_name].to_numpy()
                del df
                return data
        except Exception as e:
            raise ValueError(f"Column {col_name} not found in file {self.filepath.name}")

    def get_ch_data(self, ch: int) -> np.ndarray:
        return self.read_column(self.ch_strs[ch])

    def get_active_chs_data(self):
        if len(self.active_chs) == 1:
            return self.get_ch_data(self.active_chs[0])

        active_chs_data = ChDataDict()
        for ch in self.active_chs:
            active_chs_data[ch] = (self.get_ch_data(ch))

        return active_chs_data

    def get_dataset(self):
        file_type = self.filepath.suffix
        if file_type == ".csv":
            return pd.read_csv(self.filepath)
        elif file_type == ".pkl":
            return pd.read_pickle(self.filepath)



