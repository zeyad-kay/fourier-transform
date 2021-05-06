import ctypes
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