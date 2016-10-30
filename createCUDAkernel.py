#This code is used for converting kernels. The rest of the 
#code for this application will have the same extension as
#before

import os

#it will be used for creating a folder to put the files
cuda_path = "./CUDA_Files/"

#dictonary for substituitions on the kernel
subs = {'__kernel':'__global__', '__global':'', 
        'get_global_id': 'blockIdx * blockDim + threadIdx'}

#asks for target file, has to be opencl
opencl_name = input("Whats the OpenCL  kernel file name? ")

#checks if the name is indeed a .cl file
splited_name = opencl_name.split(".")

if not((splited_name[1] == "cl")):
    print(opencl_name + " is not a valid name. Exiting... ")
    exit()

#use with open for a more secure method
try:
    with open(opencl_name) as opencl_file:
        opencl_data = opencl_file.read()

#if something wrong happen, exit the code
except:
    print ("Not possible to open the file. Exiting...")
    exit()


#if everything works, try to create the cuda file and directory
cuda_name = ".".join([splited_name[0], "cu"])
os.mkdir("CUDA_Files")

try:
    cuda_data = open(cuda_path + cuda_name, "w")

except:
    print ("Not possible to create the file...")
    exit()


print(opencl_data)
cuda_data.close()
