# SIPHRA Analysis Tools

Set of Python tools and scripts required to test and analyze the output of the [SIPHRA ASIC](https://www.ideas.no/integrated-circuits/ide3380), used for the readout of SiPM signals.
## Analysis

All detailed analysis results and visualizations can be found in the notebooks/ directory.

## Datasets

Raw datasets are not included in this repository due to repository size constraints on GitHub. If you require the data for reproduction or further analysis, please open an issue or contact one of the collaborators directly. 

However, two sample datasets are provided in the ``data/test_data`` directory. These datasets are intended to provide an easy way to test functionalities and correspond to:

* one background radiation acquisition and 
* one acquisition performed in the presence of a $^{137}$ Cs source.

The corresponding exposure times are reported in the table below:

| **Dataset** | **Exposure (s)** |
| --- | ---: |
| Background | 164.828 
| Source | 24.934 |

> [!NOTE]
> The ``file_converters`` directory contains scripts for converting the raw datasets into a readable format. In particular, the ``ODR_DatConverter.py`` provides a comprehensive CLI tool to convert raw files into CSV or PKL formats. 
>
> The current analysis pipeline uses CSV files by default; however, this may change in the future.

## Context

This analysis is part of the prior qualification and testing for the BGO Spectrometer Unit of the [COMCUBE-S mission](https://doi.org/10.48550/arXiv.2510.24549), currently under development at KTH, Stockholm.
