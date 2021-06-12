# Fourier Transform
This is a C++ implementation of the Discrete and Fast Fourier Transforms along with building the source into a *DLL* for consuming in other languages.

There is also a python script just to demonstrate a proof of concept on how to use the *DLL* and comparing the speed of the algorithms with increasing the size of data.

__Disclaimer__: The *DLL* will probably not work on linux as *DLL* is Windows specific.

# Build
The repo already has the C++ source for the Fourier Transform and a 32-bit *DLL* already generated in the *lib/demo* folder. So for only running the demo jump
[here](#Demo).

For building the *DLL*, open the Visual Studio solution in the *lib/Fourier* folder, make your changes and build depending on your Python version (32 or 64 bit). You will find a *Fourier.dll* file in the *Debug* folder.

# Demo
To run the demo, make sure you have Python installed then:

1. From the command line create a virtual environment and activate.

```
> python -m venv .venv
> .venv\Scripts\activate
```
2. Install dependencies.
```
> pip install -r requirements.txt
```

3. Run the script.
```
> python main.py
```
In case there is an error, it is because the Python version and the *DLL* are incompatible (64-bit Python and 32-bit *DLL*). In that case, you will have to [build](#Build) a 64-bit version of the *DLL*.

4. Run the script with 
[built DLL](#Build) (optional).
```
> python main.py --debug
```

5. Run the script with the profiler
(optional).
```
> python main.py --profiler
```

# Output
Python will generate random data and compute the Fourier Transform using Numpy's implementation and the *DLL*'s implementations then print the time taken by each method with the _Mean Squared Error_ between the C++ outputs. An interactive plot will appear comparing the time taken by each method with different number of points.

Enabling the *profiler* prompts the user for the number of runs on each method.
