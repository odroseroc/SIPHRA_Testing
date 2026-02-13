from argparse import ArgumentError
from unittest import case

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

    ch_strs = [f"Ch{_}" for _ in range(17)]

    def __init__(self, dataframe:pd.DataFrame | PathLike,
                 active_chs:int | list[int],
                 exposure_sec:float,
                 sipm_chs:str | None = None,):
        '''
        summing channel is not active at the moment.
        '''
        self.dataframe = self._resolve_dataframe(dataframe)
        self.active_chs = self._resolve_active_chs(active_chs)
        self.exposure = exposure_sec
        self.sipm_chs = sipm_chs


    def _resolve_dataframe(self, f):
        try:
            f = Path(f).resolve()
            match f.suffix:
                case '.csv':
                    return pd.read_csv(f)
                case '.pkl':
                    return pd.read_pickle(f)
                case _:
                    raise NotImplementedError("Path does not point to a .csv or a .pkl file")
        except:
            if isinstance(f, pd.DataFrame):
                return f
            else:
                raise ArgumentError("The argument must be a DataFrame or a path.like object pointing to a .csv or .pkl file")

    def _resolve_active_chs(self, chs) -> list[int]:
        active_chs = []
        channels = [chs] if isinstance(chs, int) else chs
        if all(isinstance(_, int) and 1 <= _ <= 16 for _ in channels):
            return channels
        else:
            raise ValueError("active_chs should be an int or list of integers between 1 and 16")

    def get_ch_data(self, ch:int) -> np.ndarray:
        return self.dataframe[self.ch_strs[ch]].to_numpy()

    def get_active_chs_data(self):
        if len(self.active_chs) == 1:
            return self.get_ch_data(self.active_chs[0])

        active_chs_data = ChDataDict()
        for ch in self.active_chs:
            active_chs_data[ch] = (self.get_ch_data(ch))

        return active_chs_data


