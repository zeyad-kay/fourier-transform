from utils import *
import os
import numpy as np
import sys,getopt

if __name__ == "__main__":
    dll_path = os.path.join("lib","demo","Fourier.dll")
    opts, args = getopt.getopt(sys.argv[1:], "", 
                                   ["debug","profiler"])
    profiler = False
    
    for opt, arg in opts:
        # Load user generated DLL
        if opt == "--debug":
            dll_path = os.path.join("lib","Fourier","Debug","Fourier.dll")
        elif opt == "--profiler":
            profiler = True
    
    c_lib = load_dll(os.path.join(os.getcwd(),dll_path))
    
    sizes = 2**np.array(range(10,14))
    
    if profiler:
        NUMBER_OF_RUNS = int(input("Enter Number of Runs: "))
        times = profile(c_lib,sizes,NUMBER_OF_RUNS)
        mse = None
    else:
        times,mse = calc_mse(c_lib,sizes)
    plot_results(sizes,times,mse)