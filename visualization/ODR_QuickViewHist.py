import ROOT
import pandas as pd
import argparse

BITS12 =2**12
BITS

def build_parser():
    parser = argparse.ArgumentParser(
        prog='ODR_QuickViewHist',
        description='Quick histogram visualizer',
        usage='%(prog)s FILE TIME',
    )
    parser.add_argument("file",
                        help="CSV file to process",)
    parser.add_argument("-t", "--time",
                        type=float,
                        help="Exposure time in seconds. Visualize the count-rate histogram",
                        default=1.0)
    parser.add_argument("-b", "--bins",
                        tipe=int,
                        help="Number of bins for the histogram",
                        default=)
    return parser


