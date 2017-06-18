# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:46:45 2017

@author: awagner
"""
from scipy.signal import butter, filtfilt, periodogram, welch
from future.utils import lmap
import numpy as np
import pywt
import functools

"""
Butter Filter
"""

"""
Input:
    lowcut - low frequency cut
    highcut - high frequency cut
    fs - sample rate
    order - order of filter
Output:
    b - low freq paramter for filtfilt
    a - high freq paramter for filtfilt
"""


def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

"""
Input - 
    data - time signal
    lowcut - low frequency cut
    highcut - high frequency cut
    fs - sample rate
    order - order of filter
Output
    y - the signal after butter filter using lowcut and high cut, fs and order
"""
def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data-np.mean(data),padlen=25)
    return y


"""
Denoise the data with wavelet and butter 
Input:
    data - time signal
Output:
    result - signal after denosing
"""
def denoise2(data,high_cut):
    import numpy as np
    if np.std(data)<0.01:
        result = denoise(data - np.mean(data))
    else:
        result = butter_bandpass_filter(data - np.mean(data), 0.2, high_cut, 50, order=4)
    return  result



"""
Denoise the data with wavelet and 
Input:
    data - time signal
Output:
    result - signal after denosing
"""
def denoise(data):
    WC = pywt.wavedec(data,'sym8')
    threshold=0.0045*np.sqrt(2*np.log2(256))
    NWC = lmap(lambda x: pywt.threshold(x,threshold,'soft'), WC)
    return pywt.waverec( NWC, 'sym8')

"""
denoise_Sgnal
Input:
    signal_data - numpy array
Output:
    denoised_signal - numpy array of denoised rows
"""
def denoise_signal(signal_data,high_cut = 12):
#    from FunctionForPredWithDEEP import denoise2
    denoised_signal = lmap(functools.partial(denoise2, high_cut=high_cut), signal_data)
    return denoised_signal


"""
##Fused lasso for data denoiseing
Input:
    data - time signal
Output:
    result - signal after denosing
"""
def fusedlasso(sig,beta,mymatrix):   
    sig = np.reshape(sig,250)
    x = Variable(len(sig))
    #if np.std(sig)<0.05:
    #obj = Minimize(square(norm(x-sig))+tv(mul_elemwise(beta,x)))
    obj = Minimize(square(norm(x-sig))+beta*quad_form(x,mymatrix))
    prob = Problem(obj)
    prob.solve()  # Returns the optimal value.
    res = x.value
    res = np.asarray(res.flatten())
    return res[0]