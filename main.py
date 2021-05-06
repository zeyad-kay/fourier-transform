from utils import *
import os
import timeit
import numpy as np
import matplotlib.pyplot as plt
import threading
import sys,getopt

if __name__ == "__main__":
    dll_path = os.path.join("lib","demo","Fourier.dll")
    opts, args = getopt.getopt(sys.argv[1:], "", 
                                   ["debug="])
    for opt, arg in opts:
        if opt == "--debug" and arg == "True":
            dll_path = os.path.join("lib","Fourier","Debug","Fourier.dll")

    c_lib = load_dll(os.path.join(os.getcwd(),dll_path))
    
    sizes = 2**np.array(range(10,14))
    times = {
        "C++ DFT":[],
        "C++ FFT":[],
        "Numpy FFT":[]
    }

    def func_timer(func,runs,label,*args):
        time = timeit.timeit(lambda: func(*args),number=runs)
        print(f"Finished {runs} runs of {label} in {time} seconds")
        times[label].append(time)


    NUMBER_OF_RUNS = int(input("Enter Number of Runs: "))
    for N in sizes:
        print(f"Generating Random data of {N} points...")
        x = random_complex_array(size=N,seed=0)
        
        t1 = threading.Thread(target=func_timer,args=(c_ft_wrapper,NUMBER_OF_RUNS,"C++ DFT",c_lib.DFT,x))
        t2 = threading.Thread(target=func_timer,args=(c_ft_wrapper,NUMBER_OF_RUNS,"C++ FFT",c_lib.FFT,x))
        t3 = threading.Thread(target=func_timer,args=(np.fft.fft,NUMBER_OF_RUNS,"Numpy FFT",x))
        
        print(f"Computing Fourier Transform...")   
        t1.start()
        t2.start()
        t3.start()
        
        # Wait until all threads have finished
        t1.join()
        t2.join()
        t3.join()
        print()
    
    fig,ax = plt.subplots(1,1)
    fig.suptitle("Average Compute Time of Fourier Transform Algorithms for N Points")
    ax.set_xlabel("N")
    ax.set_ylabel("Time [s]")
    ax.grid(True)
    [ax.plot(sizes,value,label=key) for key,value in times.items()]
    ax.legend()
    plt.show()