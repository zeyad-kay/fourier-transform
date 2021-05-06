# Fourier Transform
This is a C++ implementation of the Discrete and Fast Fourier Transforms along with building the source into a *DLL* for consuming in other languages.

There is also a python script just to demonstrate a proof of concept of how to use the *DLL* and comparing the speed of the algorithms with increasing the size of data.

__Disclaimer__: The *DLL* will probably not work on linux as *DLL* is Windows specific.

# Build
The repo already has the C++ source for the Fourier Transform and the *DLL* already generated in the *lib/demo* folder. So for only running the demo jump
[here](#Demo).

For building the *DLL*, open the Visual Studio solution in the *lib/Fourier* folder, make your changes and build. You will find a *Fourier.dll* file in the *Debug* folder.

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

4. Run the script with 
[built DLL](#Build) (optional).
```
> python main.py --debug=True
```

# Output
You should see in the console a prompt asking for the number of runs for profiling. Then Python will generate random data and compute the Fourier Transform using Numpy's implementation and the *DLL*'s implementations then print the time taken by each method to compute the specified runs.

On completion, an interactive plot will appear comparing the time taken by each method with different number of points.