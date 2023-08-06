# cython: profile=False
import math

import numpy as np
from tslearn.metrics import dtw

cimport cython
from libc.math cimport abs, sqrt

@cython.profile(False)
cdef inline double dist(double a, double b):
    cdef double diff = a - b
    return diff * diff

@cython.profile(False)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline double array_min(double[::1] array):
    cdef double min_value = array[0]
    cdef int i
    for i in range(1, array.shape[0]):
        min_value = min_value if min_value < array[i] else array[i]
    return min_value

@cython.profile(False)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline double array_max(double[::1] array):
    cdef double max_value = array[0]
    cdef int i
    for i in range(1, array.shape[0]):
        max_value = max_value if max_value > array[i] else array[i]
    return max_value

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef whiten_multivariate(double[:,:] window_signal):
    """
    Perform whitening on signal window - it should be local to a sliding window
    """
    cdef double[:,:] s = window_signal
    result = np.empty(shape=(s.shape[1], s.shape[0]), dtype=np.float64)
    cdef double[::1,:] result_v = result.T

    cdef double mean, diff, var, std
    cdef int i, j
    for j in range(s.shape[1]):
        mean = 0
        for i in range(s.shape[0]):
            mean += s[i,j]
        mean /= s.shape[0]

        var = 0
        for i in range(s.shape[0]):
            diff = abs(mean - s[i,j])
            var += diff * diff
        var /= s.shape[0]

        std = sqrt(var)

        for i in range(s.shape[0]):
            result_v[i,j] = (s[i,j] - mean) / (std + 1e-10)

    return result.transpose()


def is_variance_ok(double[:,:] sequence, variance_thresholds):
    cdef double[:,:] s = sequence
    cdef double lower_threshold
    cdef double upper_threshold

    cdef double mean, diff, var
    cdef int i, j
    for j in range(s.shape[1]):
        mean = 0
        for i in range(s.shape[0]):
            mean += s[i,j]
        mean /= s.shape[0]

        var = 0
        for i in range(s.shape[0]):
            diff = abs(mean - s[i,j])
            var += diff * diff
        var /= s.shape[0]

        lower_threshold = variance_thresholds["lower"][j]
        upper_threshold = variance_thresholds["upper"][j]
        for i in range(s.shape[0]):
            if var < lower_threshold or var > upper_threshold:
                return False

    return True


class DTWModel(object):
    def __init__(self, window, stride, query_len, sakoeChibaWidth=0.2):
        self.window = window
        self.stride = stride
        self.sakoeChibaWidth = sakoeChibaWidth
        self.idx = self.make_envelope_index_keogh(
            query_len, window, max(1, self.sakoeChibaWidth * max(query_len, window))
        )
        self.idx = np.array(self.idx)

    def sliding_window_index(self, signal_length):
        """
        Takes length of signal and returns list of indices, each of which
        defines a sliding window
        """
        start = 0
        while (start + self.window) <= signal_length:
            yield slice(start, start + self.window)
            start += self.stride

    @staticmethod
    def distance_static(seq1, seq2, sakoeChibaWidth):
        seq1 = whiten_multivariate(seq1).transpose()
        seq2 = whiten_multivariate(seq2).transpose()
        s = 0
        if sakoeChibaWidth:
            for i in range(len(seq1)):
                dist = dtw(
                    seq1[i],
                    seq2[i],
                    global_constraint="sakoe_chiba",
                    sakoe_chiba_radius=max(1, sakoeChibaWidth * max(len(seq1[i]), len(seq2[i]))),
                )
                s += dist
        else:
            for i in range(len(seq1)):
                dist = dtw(seq1[i], seq2[i], global_constraint=None)
                s += dist
        return s

    def lb_keogh_dist(self, seq1_raw, seq2_raw, double[:,:,::1] envelope):  # seq1 is query
        cdef double[:,::1] seq1 = whiten_multivariate(seq1_raw).transpose()
        cdef double[:,::1] seq2 = whiten_multivariate(seq2_raw).transpose()
        cdef long[:,::1] idx = self.idx
        cdef double distance = 0.0
        cdef int i, j
        cdef double score1, score2, min_value, max_value
        for i in range(seq1.shape[0]):
            score1 = 0
            score2 = 0
            for j in range(seq2.shape[1]):
                if seq2[i][j] < envelope[i][j][1]:
                    score1 += dist(seq2[i,j], envelope[i,j,1])
                elif seq2[i][j] > envelope[i][j][0]:
                    score1 += dist(seq2[i][j], envelope[i][j][0])
            for j in range(seq1.shape[1]):
                max_value = array_max(seq2[i][idx[j,0] : idx[j,1]])
                min_value = array_min(seq2[i][idx[j,0] : idx[j,1]])
                if seq1[i,j] < min_value:
                    score2 += dist(seq1[i,j], min_value)
                if seq1[i,j] > max_value:
                    score2 += dist(seq1[i,j], max_value)
            distance += max(sqrt(score1), sqrt(score2))

        return distance

    def make_envelope_keogh(self, seq, sz2, radius):
        ix = self.make_envelope_index_keogh(sz2, len(seq), radius)
        res = []
        for item in ix:
            res.append((max(seq[item[0] : item[1]]), min(seq[item[0] : item[1]])))
        return res

    @staticmethod
    def make_envelope_index_keogh(sz1, sz2, radius):
        res = []
        if sz1 == 1:
            return [(0, sz2)]
        ratio = (sz2 - 1) / (sz1 - 1)
        for i in range(sz1):
            res.append((max(math.ceil(i * ratio - radius), 0), math.floor(i * ratio + radius) + 1))

        return res

