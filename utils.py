import ctypes
import threading
import timeit
from time import perf_counter
from matplotlib import pyplot as plt
import numpy as np

def random_complex_array(size,seed=None):
    """
    Generate a random numpy complex array.
    Omitting seed parameter returns same random array.
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.rand(size).astype(np.double) + np.random.rand(size).astype(np.double)*1j

def reshape_complex_array(arr):
    """
    Make numpy complex array compatible
    with C++ STL complex type
    """
    new_np = []
    if arr.size == 0:
        return arr
    for x in arr:
        new_np.append(x.real)
        new_np.append(x.imag)     
    return np.array(new_np,dtype=np.double)

def load_dll(path):
    return ctypes.CDLL(path)

def c_ft_wrapper(Func,data):
    """
    Return the Fourier Transform of data using a function loaded from a DLL.
    Supported functions are DFT and FFT.
    """
    if data.size == 0:
        return data

    Func.argtypes = [np.ctypeslib.ndpointer(ctypes.c_double,ndim=1,flags="C_CONTIGUOUS"),ctypes.c_long]
    Func.restype = ctypes.POINTER(ctypes.c_double)
    
    # Make numpy complex array compatible
    # with C++ STL complex type
    data = reshape_complex_array(data)
    result = Func(data,int(data.size / 2))
    np_result = np.ctypeslib.as_array(result,(int(data.size/2),2))

    # Make array compatible with numpy structure
    return np_result[:,0] + np_result[:,1]*1j

def plot_times(sizes,times):
    fig,ax = plt.subplots(1,1)
    fig.suptitle("Average Compute Time of Fourier Transform Algorithms for N Points")
    ax.set_xlabel("N")
    ax.set_ylabel("Time [s]")
    ax.grid(True)
    [ax.plot(sizes,value,label=key) for key,value in times.items()]
    ax.legend()
    plt.show()

def regular(c_lib,sizes):
    """
    Run Fourier Transform functions once and 
    calculate the Mean Squared Error
    """
    times = {
        "C++ DFT":[],
        "C++ FFT":[],
        "Numpy FFT":[]
    }

    def func_timer(func,label,*args):
        start = perf_counter()
        ft = func(*args)
        stop = perf_counter()
        t = stop - start
        print(f"Finished {label} in {t} seconds")
        times[label].append(t)
        return ft

    for N in sizes:
        print(f"Generating Random data of {N} points...")
        x = random_complex_array(size=N)
        
        print(f"Computing Fourier Transform...")
        np_fft = func_timer(np.fft.fft,"Numpy FFT",x)
        c_fft = func_timer(c_ft_wrapper,"C++ FFT",c_lib.FFT,x)
        c_dft = func_timer(c_ft_wrapper,"C++ DFT",c_lib.DFT,x)
        MSE = np.square(np.subtract(c_fft,c_dft)).mean()

        print(f"Mean Squared Error: {MSE}")
        print()
    return times

def profile(c_lib,sizes,runs):
    """
    Profile Fourier Transform functions for a number of runs.
    """
    times = {
        "C++ DFT":[],
        "C++ FFT":[],
        "Numpy FFT":[]
    }

    def func_timer(func,runs,label,*args):
        time = timeit.timeit(lambda: func(*args),number=runs)
        print(f"Finished {runs} runs of {label} in {time} seconds")
        times[label].append(time)

    for N in sizes:
        print(f"Generating Random data of {N} points...")
        x = random_complex_array(size=N)
        
        t1 = threading.Thread(target=func_timer,args=(c_ft_wrapper,runs,"C++ DFT",c_lib.DFT,x))
        t2 = threading.Thread(target=func_timer,args=(c_ft_wrapper,runs,"C++ FFT",c_lib.FFT,x))
        t3 = threading.Thread(target=func_timer,args=(np.fft.fft,runs,"Numpy FFT",x))
        
        print(f"Computing Fourier Transform...")   
        t1.start()
        t2.start()
        t3.start()
        
        # Wait until all threads have finished
        t1.join()
        t2.join()
        t3.join()
        print()
    return times