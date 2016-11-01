#This code is used for converting kernels. The rest of the 
#code for this application will have the same extension as
#before

import os

#it will be used for creating a folder to put the files
cuda_path = "./CUDA_Files/"

#dictonary for substituitions on the kernel
subs_cl = {'__global':'', '__kernel':'__global__', 
        'get_global_id(0)': 'blockIdx * blockDim + threadIdx'}

#asks for target file, has to be opencl
opencl_name = input("Whats the OpenCL  kernel file name? ")
main_name = input("Whats the C/C++ file name? ")

#checks if the name is indeed a .cl file
splited_name = opencl_name.split(".")

if not((splited_name[1] == "cl")):
    print(opencl_name + " is not a valid name. Exiting... ")
    exit()
#i'm doing separated try/except in order to find the problems
#use with open for a more secure method
try:
    opencl_data = open(opencl_name, 'r') 

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

#replacing the dict items
for line in opencl_data:
    for key, value in subs_cl.items():
        line = line.replace(key,value)
    cuda_data.write(line)

opencl_data.close()
cuda_data.close()
