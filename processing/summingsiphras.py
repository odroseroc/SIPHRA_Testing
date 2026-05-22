import numpy as np

def match_events(sec1, subsec1, sec2, subsec2, tolerance=999):
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

    sec1 = np.array(sec1)
    subsec1 = np.array(subsec1)
    sec2 = np.array(sec2)
    subsec2 = np.array(subsec2)

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
    return matched, unmatched1, unmatched2

if __name__ == '__main__':
    #Testing
    sec1 = [100, 100, 101, 102]
    subsec1 = [12345, 67890, 11111, 54321]
    sec2 = [100, 100, 101, 103]
    subsec2 = [12400, 67999, 11050, 99999] # 12400 ~ 12345, 67999 ~ 67890, etc.

    matched, unmatched1, unmatched2 = match_events(sec1, subsec1, sec2, subsec2)

    print("Matched events:")

    for i, j in matched:
        print(f" Det1[{i}]: sec={sec1[i]}, subsec={subsec1[i]}"
            f" <--> Det2[{j}]: sec={sec2[j]}, subsec={subsec2[j]}"
            f" | Δsubsec = {abs(subsec1[i] - subsec2[j])}")

    print(f"\nNo partner in detector 1 index: {unmatched1}")
    print(f"No partner in detector 2 index: {unmatched2}")