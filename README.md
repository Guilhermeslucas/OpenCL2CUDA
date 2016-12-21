# OpenCL2CUDA
This is just a attempt to create a helper to convert .cl
apliccations to CUDA applications. At first, it will perform
a bunch of changes in code, searching for OpenCL words and 
writing its equivalent on .cu files.

This is part of my work at the OpenPower Foundation Lab at
Unicamp. More work avaiable at the following link:
```
http://openpower.ic.unicamp.br/
```

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

Note: some of the changes on the main code are suggestions of, for example, 
equivalences between OpenCL and CUDA or OpenCL functions that are not need anymore.
To find these statements, you can use the search engine from your text editor and
search for the word 
```
#translation#
```

We have these examples below fully working:

***-Vector add:***
```
https://github.com/Guilhermeslucas/SDAccel_Examples/tree/master/getting_started/vadd
```

You can contribute to the software forking it, asking for pull request,
sending me more OpenCL and CUDA tips. For now, if you have some code
with the same function written in OpenCL and CUDA, It would help me
a lot.
