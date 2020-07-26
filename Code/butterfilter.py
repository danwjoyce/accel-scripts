# implementation of butterworth filter (adapted from : https://stackoverflow.com/a/25192640)

import numpy as np
from scipy.signal import butter, lfilter, freqz

def butter_bandpass(lo_cutoff, hi_cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_lo_cutoff = lo_cutoff / nyq
    normal_hi_cutoff = hi_cutoff / nyq
    # use digital filter as constant sample frequency
    b, a = butter(order, [normal_lo_cutoff, normal_hi_cutoff], btype='bandpass', analog=False)
    return b, a

def butter_bandpass_filter(data, lo_cutoff, hi_cutoff, fs, order=4):
    b, a = butter_bandpass(lo_cutoff, hi_cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
