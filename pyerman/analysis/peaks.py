from __future__ import division, print_function
import numpy as np

def detect_peaks(x, min_height=None, min_distance=1,
        min_dx=0, edge='rising',kpsh=False):

    """
    Peak finding.

    :param x: 1D Arraylike data
    :param min_height: Minimum Peak Height
    :param min_distance: Minimum peak (inter)distance
    :param min_dx: minimum dx between peaks and neighboring points
    :param edge: For flat peaks, detect rising , falling both or none of the points.
    :param kpsh: If adjascent peaks are closer than min_distance, keep both  if same height

    :returns: 1D Arraylike with indices of peaks
    """

    # Type safety
    x = np.atleast_1d(x).astype('float64')
    # Small arrays get skipped
    if x.size < 3:
        return np.array([], dtype=int)
    dx = x[1:] - x[:-1]
    # Turn NaNs into inf
    nans = np.where(np.isnan(x))[0]
    if nans.size:
        x[nans] = np.inf
    # First derivative
    dx = x[1:] - x[:-1]
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and nans.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((nans, nans-1, nans+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and min_height is not None:
        ind = ind[x[ind] >= min_height]
    # remove peaks - neighbors < min_dx
    if ind.size and min_dx > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < min_dx)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and min_distance > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - min_distance) & (ind <= ind[i] + min_distance) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    return ind
