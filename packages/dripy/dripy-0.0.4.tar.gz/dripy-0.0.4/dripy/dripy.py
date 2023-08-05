"""
--------------------------------------------------------------------------
Description
--------------------------------------------------------------------------
dripy is a set of python tools for manipulating drilling data

--------------------------------------------------------------------------
Author
--------------------------------------------------------------------------
Ben Thornton (ben.thornton@mscsofware.com)
Simulation Consultant - MSC Software

--------------------------------------------------------------------------
Version
--------------------------------------------------------------------------
v1 - 20181120

"""
from scipy import signal

def pason_post_processing(t,sig):
    """
    Process a signal as it would be processed by pason
    
    Parameters
    ----------
    t : list
        Time series corresponding to the signal to be processed
    
    sig : list
        Signal to be processed
                  
    Returns
    -------
    tuple
        time, processed signal
    """
    # (1) Sample at 50 Hz
    f = 50
    num = int((t[-1] - t[0])*f + 1)
    sig_1, t_1 = signal.resample(sig,num,t)

    # (2) 0.99 Hz Digital Low Pass Filter
    f_c = 0.99
    f_s = 1/(t_1[1]-t_1[0])
    W = f_c/f_s*2
    b,a = signal.butter(5, W)
    t_2 = t_1
    sig_2 = list(signal.filtfilt(b, a, sig_1))

    # (3) resample at 5 Hz
    f = 5
    num = int((t_2[-1] - t_2[0])*f + 1)
    sig_3, t_3 = signal.resample(sig_2,num,t_2)

    # (4) calculate maximum over each 1 sec period
    t_4 = [t_3[0]]
    sig_4 = [0]
    counter = 0
    for i in range(len(t_3)):
        if counter == 5:
            t_4.append(t_3[i])
            sig_4.append(max(sig_3[i-5:i]))
            counter = 0

        counter += 1

    # set the first value equal to the second value to make the line look nice
    sig_4[0] = sig_4[1]

    return t_4, sig_4
