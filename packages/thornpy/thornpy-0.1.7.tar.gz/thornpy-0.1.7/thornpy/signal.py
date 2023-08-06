"""Signal processing module
"""
from scipy.signal import butter, filtfilt

def low_pass(sig, time, freq_cutoff, N=5):
    """Applies a Nth order butterworth lowpass filter.
    
    Parameters
    ----------
    sig : list
        Signal to be filtered
    time : list
        Time signal associated with `sig`
    freq_cutoff : int
        Cutoff frequency to use when filtering
    N : int
        Order of butterworth filter (default is 5)
    
    Returns
    -------
    list
        Filtered signal
    list
        Time signal associated with filtered signal

    """
    freq_samp = 1/(time[1]-time[0])
    omega = freq_cutoff/freq_samp*2
    b_coef, a_coef = butter(N, omega)
    return list(filtfilt(b_coef, a_coef, sig)), time
    