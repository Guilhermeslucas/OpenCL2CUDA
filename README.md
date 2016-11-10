# OpenCL2CUDA
This is just a attempt to create a helper to convert .cl
apliccations to CUDA applications. At first, it will perform
a bunch of changes in code, searching for OpenCL words and 
writing its equivalent on .cu files.

The files I'm using for testing are in this repository:

```
https://github.com/Guilhermeslucas/SDAccel_Examples
```
You can find more examples there, if you want.

Note: This is not a full converter (at least at this point).
It just helps you with a lot of replacements, but you still need
to look the generated files to ensure the full and correct work of
your code.

## Running the aplication
I'm using python3 to run the code. 
All you have to do is (on GNU/Linux OS's):

```
chmod +x createCUDAkernel.py (just the first time)
./createCUDAkernel.py --opencl_name="name of the opencl file" --main_name="name of the C/C++ file"
```
