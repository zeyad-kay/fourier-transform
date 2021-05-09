import ctypes
import threading
import timeit
from time import perf_counter
from matplotlib import pyplot as plt
import numpy as np

def random_complex_array(size,seed=None):
    """Generate a random numpy complex array.
    Omitting seed parameter returns same random array.

    Args:
        size (integer): number of points
        seed (integer, optional): seed for predicatble random data. Defaults to None.

    Returns:
        numpy array: array of complex data
    """    
    if seed is not None:
        np.random.seed(seed)
    return np.random.rand(size).astype(np.double) + np.random.rand(size).astype(np.double)*1j

def reshape_complex_array(arr):
    """Make numpy complex array compatible
    with C++ STL complex type

    Args:
        arr (numpy array): array of complex data 

    Returns:
        numpy array: reshaped numpy array
    """    
    new_np = []
    if arr.size == 0:
        return arr
    for x in arr:
        new_np.append(x.real)
        new_np.append(x.imag)     
    return np.array(new_np,dtype=np.double)

def load_dll(path):
    """Loads C library

    Args:
        path (string): path to DLL

    Returns:
        CDLL: Loaded DLL
    """    
    return ctypes.CDLL(path)

def c_ft_wrapper(Func,data):
    """
    Return the Fourier Transform of data using a function loaded from a DLL.
    Supported functions are DFT and FFT.
    
    Args:
        Func (function): C fourier transform function 
        data (numpy array): data to perform fourier transform

    Returns:
        numpy array: fourier transform of the data
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

def plot_results(sizes,times,mse=None):
    """Plot time and size

    Args:
        sizes (array): data sizes
        times (dictionary): dictionary of times of each method
        mse (array, optional): Mean Square Error of every size
    """
    if mse is not None:
        fig,ax = plt.subplots(1,2)
        fig.suptitle("Average Compute Time and Mean Square Error of Fourier Transform Algorithms for N Points")
        ax[0].set_xlabel("N")
        ax[1].set_xlabel("N")
        ax[0].set_ylabel("Time [s]")
        ax[1].set_ylabel("Mean Square Error")
        ax[0].grid(True)
        ax[1].grid(True)
        [ax[0].plot(sizes,value,label=key) for key,value in times.items()]
        ax[1].plot(sizes,mse)
        ax[0].legend()
    else:
        fig,ax = plt.subplots(1,1)
        fig.suptitle("Average Compute Time of Fourier Transform Algorithms for N Points")
        ax.set_xlabel("N")
        ax.set_ylabel("Time [s]")
        ax.grid(True)
        [ax.plot(sizes,value,label=key) for key,value in times.items()]
        ax.legend()

    plt.show()

def calc_mse(c_lib,sizes):
    """Run Fourier Transform functions once and 
    calculate the Mean Squared Error

    Args:
        c_lib (CDLL): loaded C library
        sizes (array): array of data sizes to compute fourier transform

    Returns:
        dictionary: dictionary of times of each method
    """    
    times = {
        "C++ DFT":[],
        "C++ FFT":[],
        "Numpy FFT":[]
    }
    mse = []

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
        mse.append(MSE)
        print(f"Mean Squared Error: {MSE}")
        print()
    return times,np.abs(mse)

def profile(c_lib,sizes,runs):
    """Profile Fourier Transform functions for a number of runs.

    Args:
        c_lib (CDLL): loaded C library
        sizes (array): array of data sizes to compute fourier transform
        runs (integer): number of times to repeat the function

    Returns:
        dictionary: dictionary of times of each method
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