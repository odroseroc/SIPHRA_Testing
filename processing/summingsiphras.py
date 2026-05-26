import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def match_events(file1, file2, output_path="matched_events.csv", tolerance=999):
    """Matches events from two detectors based on temporal proximity.
    Parameters:
        sec1, subsec1: lists of seconds and subseconds from detector 1
        sec2, subsec2: lists of seconds and subseconds from detector 2
        tolerance: maximum difference in subseconds to consider as the same event (default 999, covers the last 3
        digits in 5-digit data)
    Returns:
        matched: list of tuples (i, j) with matched indices
        unmatched1: unmatched indices from detector 1 pair
        unmatched2: unmatched detector 2 indices"""

    sec1 = np.array(file1['Time_sec'])
    subsec1 = np.array(file1['Time_sub'])
    sec2 = np.array(file2['Time_sec'])
    subsec2 = np.array(file2['Time_sub'])

    matched = []
    used2 = set()

    seconds_common = np.intersect1d(sec1, sec2)

    for s in seconds_common:
        idx1 = np.where(sec1 == s)[0]
        idx2 = np.where(sec2 == s)[0]

        for i in idx1:
            idx2_free = [j for j in idx2 if j not in used2]
            if not idx2_free:
                continue
            diffs = np.abs(subsec1[i] - subsec2[idx2_free])
            min_pos = np.argmin(diffs)
            if diffs[min_pos] <= tolerance:
                j = idx2_free[min_pos]
                matched.append((i, j))
                used2.add(j)
    used1 = {i for i, _ in matched}
    unmatched1 = [i for i in range(len(sec1)) if i not in used1]
    unmatched2 = [j for j in range(len(sec2)) if j not in used2]

    matched_rows = []

    for i, j in matched:

        row1 = file1.iloc[i]
        row2 = file2.iloc[j]

        combined = {}

        # Add detector 1 columns
        for col in file1.columns:
            combined[f"A_{col}"] = row1[col]

        # Add detector 2 columns
        for col in file2.columns:
            combined[f"B_{col}"] = row2[col]

        # Add timing difference
        combined["subsec_difference"] = abs(
            row1["Time_sub"] - row2["Time_sub"]
        )

        matched_rows.append(combined)

    matched_df = pd.DataFrame(matched_rows)

    matched_df.to_csv(output_path, index=False)

    print(f"Saved {len(matched_df)} matched events to:")
    print(output_path)

    return matched_df

    #return matched, unmatched1, unmatched2

if __name__ == '__main__':
    filepath_A = "../data/260519/A_SUBT_02_NewSourceTest_Cs137.csv"
    filepath_B = "../data/260519/B_SUBT_02_NewSourceTest_Cs137.csv"

    file_A = pd.read_csv(filepath_A)
    file_B = pd.read_csv(filepath_B)

    matched_df = match_events(file_A, file_B)

    print(matched_df.head())

