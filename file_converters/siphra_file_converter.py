from pathlib import Path
import sys
import os
import numpy as np
import pandas as pd
from d2a_decoder import D2a
from kaitaistruct import KaitaiStream, ValidationNotEqualError

pt100_calib = [(2132.45, 0.029005),
               (2342.96, 0.029048),
               (2069.69, 0.028884),
               (2171.65, 0.029113)]

crystal_id = ['A', 'B', 'C', 'D']

pt100_calib = np.asarray(pt100_calib).T


def temp(x, a, b):
    res = 100 + (x - b) * a
    return -245 + 2.3519 * res + 0.00103 * (res * res)


def process_events(f, crystal_code):
    p, n = os.path.split(f)
    b, e = os.path.splitext(n)
    filepath = f
    # newpath = f'{p}/ROOT_FILES'
    # if not os.path.exists(newpath):
    #    os.makedirs(newpath)

    i = 0
    with open(f, 'rb') as test_file:
        while test_file.read(4) != b"\xC2\x10\x00\x00":
            i += 4
            test_file.seek(i)
            if i > 128:
                raise Exception('File is corrupted or format is invalid')
    size = os.path.getsize(f)
    num_events = int(size / 64)

    io = KaitaiStream(open(f, 'rb'))  # Open data file in streaming mode
    io.seek(i)

    data = np.empty((num_events, 23), dtype=np.uint32)
    j = 0
    while io is not None:
        try:
            data[j] = D2a.Event(io).ret
            j += 1
        except ValidationNotEqualError:
            print('seeking')
            print(io.pos())
        except EOFError:
            break

    i = crystal_code

    det_a_events = data[data[:, 0] == 5 + i]
    det_a_external = det_a_events[det_a_events[:, 2] < 25]
    det_a_internal = det_a_events[det_a_events[:, 2] > 25]
    det_a_baselines = np.mean(det_a_internal[:, 6:], axis=0)
    det_a_master_external = np.zeros((np.shape(det_a_external)[0], (np.shape(det_a_external)[1] + 2)))
    det_a_master_external[:, :-2] = det_a_external
    # det_a_master_external[:,6:-2] -= det_a_baselines
    det_a_master_external[:, -2] = np.argmax(det_a_master_external[:, 7:-2], axis=1) + 1
    det_a_master_external[:, -1] = np.sum(det_a_master_external[:, 7:-2], axis=1)
    det_a_T = det_a_master_external.T

    dataset = pd.DataFrame({'Detector': det_a_T[0],
                            'ID': det_a_T[1],
                            'Trigger': det_a_T[2],
                            'Time_sub': det_a_T[3],
                            'Time_sec': det_a_T[4],
                            'Time_gps': det_a_T[5],
                            'Temp': temp(det_a_T[6], pt100_calib[1, i], pt100_calib[0, i]),
                            'Ch1': det_a_T[7],
                            'Ch2': det_a_T[8],
                            'Ch3': det_a_T[9],
                            'Ch4': det_a_T[10],
                            'Ch5': det_a_T[11],
                            'Ch6': det_a_T[12],
                            'Ch7': det_a_T[13],
                            'Ch8': det_a_T[14],
                            'Ch9': det_a_T[15],
                            'Ch10': det_a_T[16],
                            'Ch11': det_a_T[17],
                            'Ch12': det_a_T[18],
                            'Ch13': det_a_T[19],
                            'Ch14': det_a_T[20],
                            'Ch15': det_a_T[21],
                            'Ch16': det_a_T[22],
                            'Argmax': det_a_T[23],
                            'Summed': det_a_T[24]}, dtype=np.float64)

    # dataset.to_pickle(f'{newpath}/{n}.CRYSTAL{crystal_id[i]}.pkl')
    # dataset.to_pickle(f'{n}.CRYSTAL{crystal_id[i]}.pkl')
    # dataset.to_pickle(f'{n}.pkl')
    output = filepath.with_suffix('.csv')
    dataset.to_csv(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print()
        print("Error! Please pass Siphra data file as argument!")
        print()
        sys.exit(1)

    folder =  Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        raise FileNotFoundError(f"File \"{sys.argv[1]}\" does not exist!")

    verbose = False
    if len(sys.argv) == 3:
        verbose = True if sys.argv[2] == "-v" else False

    file_qty = sum(1 for _ in folder.glob("*.dat"))
    if file_qty == 0:
        raise FileNotFoundError(f"No suitable (.dat) files found in \"{sys.argv[1]}\" for conversion!")

    print()
    print(f"{file_qty} files found. Starting processing...")

    for f in folder.glob("*.dat"):
        if verbose:
            print()
            print(f"Target file \"{f.name}\" found.")
            print("Processing...")

        process_events(f, 0)

        if verbose:
            print(f"Wrote file \"{f.parent}.csv\"!")

    print()
    print(f"Done! {file_qty} files converted to CSV.")
    print()









