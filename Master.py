import multiprocessing
import sys
import os
from utils import *
from DataKeeper import DataKeeper
from MasterClient import MasterClient
from MasterDK_Rep import MasterDK_Rep
from MasterDK_Alive import MasterDK_Alive

manager = multiprocessing.Manager()
dataKeepers = manager.dict() 
files_metadata = manager.dict()

# Generate Ports for master processes
for i in range(50002 , 50002 + masterNumOfProcesses):
    masterPortsArr.append(str(i))

ports = {}
# Generate Ports for all data keepers processes
for j in range(30002 , 30002 + dataKeeperNumOfProcesses):
        ports[str(j)] = Port(str(j))
        dataKeeperPorts.append(str(j))

for ip in dataKeepersIps:
    dataKeepers[ip] = DataKeeper(ip, ports)
    


processes = []
# Keep DK alives Process
p = multiprocessing.Process(target = MasterDK_Alive, args=(dataKeepers,)) # launch a process which will increment every value of s_arr
processes.append(p) # remember it
p.start() #...and run!

# N-Replicates Process
p = multiprocessing.Process(target = MasterDK_Rep, args=(dataKeepers, files_metadata,)) # launch a process which will increment every value of s_arr
processes.append(p) # remember it
p.start() #...and run!

# Client & DK Processes
for x in range(masterNumOfProcesses):
    p = multiprocessing.Process(target = MasterClient, args=(dataKeepers,files_metadata, masterPortsArr[x])) # launch a process which will increment every value of s_arr
    processes.append(p) # remember it
    p.start() #...and run!

# Wait for every process to end
for p in processes:
    p.join()
