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
#        - Copy from host, copy to host                              #
#        - Decide what to do with unecessary OpenCL functions        #
###################################################################### 

import argparse
import os
import glob
from operator import itemgetter

#list to place the memories that will be used to call kernel call
device_memory = []

#function to crate the cuda kernell call 
def treat_kernelCall(line,kernel_name,device_memory):
    splited = line.split(',')
    device_memory = sorted(device_memory, key=itemgetter(0))

    #gets the grid and block size, to make the full kernel call
    grid_size = splited[4].replace('&','')
    block_size = splited[5].replace('&','')
    
    #to keep the code pretty, i'll have to maintain identation
    begin = '' 
    for char in list(splited[0]):
        #if the character is a identing one, 
        if (char == '\t' or char == ' '):
            begin = begin + char
        else:
            break

    #this part is necessary to construct the arguments for kernel call
    arguments = [] 
    for index,argument in device_memory:
        arguments.append(str(argument))
    
    #concatenates everything
    arguments = ','.join(arguments)
    
    return (begin+kernel_name+'<<<'+grid_size+','+block_size+'>>>('+arguments+')\n')

#this is the function to treat the device memories that will
#be passed to the kernel call
def treat_deviceMemory(line):
    splited = line.split(',')
    argument_index = int(splited[1])
    
    #this is kind of bad, i'll change this later
    listed_variable = splited[3].split('&')
    almost_parsed = listed_variable[len(listed_variable) - 1]
    
    #after spliting on &, the last element is the variable name, just
    #nedd to find the ) to get the full variable name
    variable_name = almost_parsed[0:almost_parsed.index(')')]
    
    #append in order to have all the argument name and position later
    device_memory.append([argument_index,variable_name])

#create buffer is bit difference, so have to special treated
def treat_createBuffer(line):
    splited = line.split(',')
    #one argument of cudaMalloc is the size, that is the third argument
    #on createBuffer. we also have to allocate the variable name
    size = splited[2]
    #i have to do this to maintain identation
    begin_line = ''
    variable_name = ''
    for char in list(splited[0]):
        #no more indentation or variable name tobe construct
        if (char == '='):
            break
        #contruct identation
        elif (char == '\t' or char == ' '):
            begin_line = begin_line + char
        #construct variable name
        else:
            variable_name = variable_name + char
    
    #join all the characters that initiate the line
    begin_line = ''.join(list(begin_line))
    return begin_line + 'cudaMalloc(&' + variable_name + ',' + size + ')\n' 

def treat_createKernel(line):
    splited = line.split(',')
    kernel_name = splited[1].replace('"','')
    return kernel_name

print ("Beginning of the Script")

#it will be used for creating a folder to put the files
cuda_path = "./CUDA_Files_1/"

#dictonary for substituitions on the kernel
#so hardcoded, i'll change it later
subs_cl = {'__global ':' ',
            'get_global_id(0)': 'blockIdx.x * blockDim.x + threadIdx.x',
            'get_num_groups(0)':'gridDim.x',
            'get_num_groups(1)': 'gridDim.y', 
            'get_num_groups(2)': 'gridDim.z',
            'get_local_size(0)': 'blockDim.x',
            'get_local_size(1)': 'blockDim.y',
            'get_local_size(2)': 'blockDim.z', 
            'get_group_id(0)': 'blockIdx.x',
            'get_group_id(1)': 'blockIdx.y',
            'get_group_id(2)': 'blockIdx.z',
            'get_local_id':'threadIdx', '__kernel':'__global__'}

#dictonary for changes on the main aplication
#kind of big, I intend to change this later
subs_main  = {'clReleaseMemObject': 'cudaFree',
              'cl_device_id': 'CUdevice', 'cl_context': 'CUcontext',
              'cl_program': 'CUmodule', 'cl_kernel': 'CUfunction',
              'cl_mem': 'CUdeviceptr', 'get_num_goups()': 'gridDim',
              'get_local_size()': 'blockDim', 
              'get_group_id()': 'blockIDx', 
              'get_local_id()': 'threadIdx',
              'clGetContextInfo': 'cuDeviceGet',
              'clCreateContextFromType':'cuCtxCreate',
              'clEnqueWriteBuffer': 'cuMemcpyHtoD',
              'clEnqueuedNDRangeKernel': 'cuLaunchGrid',
              'cl_command_queue': 'cudaStream_t', 'cl_event': 'cudaEvent_t',
              'cl_image_format': 'cudaChannelFormatDesc'}

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
    print("Your files will be created on folder "+cuda_path.split("/")[1])

#creating the main file to be the resulting one
main_cuda_name = splited_name_main[0]+"_cuda.cu"

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
        #removing the include opencl libraris. not the best way,but works
        if ('opencl.h' in line):
            line = ' '
            break
        #getting arguments for device
        elif ('clCreateBuffer' in line):
            line = treat_createBuffer(line)
            break
        #will be used to know the kernel call parameters
        elif ('clSetKernelArg' in line):
            treat_deviceMemory(line)
            line = ' '
            break
        #getting kernel function name
        elif ('clCreateKernel' in line):
            kernel_name = treat_createKernel(line)
            line = ' '
            break
        #creates the cuda kernell call
        elif ('clEnqueueNDRangeKernel' in line):
            line = treat_kernelCall(line, kernel_name, device_memory)
            break
        #else, just replace the words
        else:
            line = line.replace(key,value)
    main_data_write.write(line)

#closes everything
main_data.close()
opencl_data.close()
cuda_data.close()
main_data_write.close()

print("Everything worked well")
print("Don't forget to include library with -L and includes with -I for the CUDA path. Its usually on /usr/local/cuda/ ")
