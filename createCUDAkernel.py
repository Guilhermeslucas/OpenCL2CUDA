#!/usr/bin/python3

########################################################################
# Copyright 2016 Guilherme Lucas da Silva (guilherme.slucas@gmail.com) #
#                                                                      #
# Licensed under the Apache License, Version 2.0 (the “License”);      #
# you may not use this file except in compliance with the License.     #
# You may obtain a copy of the License at                              #
#                                                                      #
# http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                      #
# Unless required by applicable law or agreed to in writing, software  #
# distributed under the License is distributed on an “AS IS” BASIS,    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or      #
# implied.                                                             #
# See the License for the specific language governing permissions and  #
# limitations under the License.                                       #
#                                                                      #
########################################################################

######################################################################
# To do: - treat non direct equivalences                             #
#        - treat the threads problem on the kernel subs              #
###################################################################### 

import argparse
import os
import glob

print ("Beginning of the Script")

#it will be used for creating a folder to put the files
cuda_path = "./CUDA_Files_1/"

#dictonary for substituitions on the kernel
subs_cl = {'__global':' ',
            'get_global_id(0)': 'blockIdx * blockDim + threadIdx',
            '__kernel':'__global__', 'get_num_groups(0)':'gridDim.x',
            'get_num_groups(1)': 'gridDim.y', 
            'get_num_groups(2)': 'gridDim.z',
            'get_local_size(0)': 'blockDim.x',
            'get_local_size(1)': 'blockDim.y',
            'get_local_size(2)': 'blockDim.z', 
            'get_group_id(0)': 'blockIdx.x',
            'get_group_id(1)': 'blockIdx.y',
            'get_group_id(2)': 'blockIdx.z',
            'get_local_id':'threadIdx'}

#dictonary for changes on the main aplication
subs_main  = {'clReleaseMemObject': 'cudaFree',
              'cl_device_id': 'CUdevice', 'cl_context': 'CUcontext',
              'cl_program': 'CUmodule', 'cl_kernel': 'CUfunction',
              'cl_mem': 'CUdeviceptr', 'get_num_goups()': 'gridDim',
              'get_local_size()': 'blockDim', 
              'get_group_id()': 'blockIDx', 
              'get_local_id()': 'threadIdx',
              'clGetContextInfo': 'cuDeviceGet',
              'clCreateContextFromType':'cuCtxCreate',
              'clCreateKernel': 'cuModuleGetFunction',
              'clCreateBuffer': 'cuMemAlloc',
              'clEnqueWriteBuffer': 'cuMemcpyHtoD',
              'clSetKernelArg': 'cuParamSeti',
              'clEnqueuedNDRangeKernel': 'cuLaunchGrid'}

#Uses argparse to receive the input information
parser = argparse.ArgumentParser()
parser.add_argument('--opencl_name', type=str, default='none',
                    help='Whats the CL kernel file name? ')

parser.add_argument('--main_name', type=str, default='none',
                    help='Whats the C/C++ file name? ')

args = parser.parse_args()

#checks if the name is indeed a .cl file
splited_name_cl = args.opencl_name.split(".")
splited_name_main = args.main_name.split(".")

#this part of the code checks the extensions of the files
if not((splited_name_cl[1] == "cl")):
    print(args.opencl_name + " is not a valid name. Exiting... ")
    exit()

if not((splited_name_main[1] == "c" or splited_name_main[1] == "cpp")):
    print(args.main_name + "is not a valid name. Exiting... ")
    exit()

#i'm doing separated try/except in order to find the problems
#use with open for a more secure method
try:
    opencl_data = open(args.opencl_name, 'r') 

#if something wrong happen, exit the code
except:
    print ("Not possible to open the opencl kernel. Exiting...")
    exit()

#try to open the main data to read
try:
    main_data = open(args.main_name, 'r')

except:
    print ("Not possible to open the main file to read. Exiting... ")
    exit()

#if everything works, try to create the cuda file and directory
cuda_name = ".".join([splited_name_cl[0], "cu"])

try:
    os.mkdir("CUDA_Files_1")

#iterates until find a valid name
except:
    folders = glob.glob("CUDA_Files*")
    folders = sorted(folders)
    cuda_path = "./CUDA_Files_" + str(len(folders) + 1) + '/'
    os.mkdir(cuda_path)
    print("Your files will be created on " + cuda_path)

#creating the main file to be the resulting one
main_cuda_name = splited_name_main[0]+"_cuda."+splited_name_main[1]

#try to create the file to be the main converted file
try:
    main_data_write = open(cuda_path + main_cuda_name, "w")

except:
    print("Not possible to create main cuda file. Exiting... ")
    exit()
    
#try to create the file to be the cuda kernel
try:
    cuda_data = open(cuda_path + cuda_name, "w")

except:
    print ("Not possible to create the kernel file...")
    exit()

#replacing the dict items
for line in opencl_data:
    for key, value in subs_cl.items():
        line = line.replace(key,value)
    cuda_data.write(line)

#replacing the words on the main code
for line in main_data:
    for key, value in subs_main.items():
        line = line.replace(key,value)
    main_data_write.write(line)


#closes everything
main_data.close()
opencl_data.close()
cuda_data.close()
main_data_write.close()

print("Everything worked well")
