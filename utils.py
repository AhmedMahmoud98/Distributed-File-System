import socket
from contextlib import closing
from math import ceil
import pickle
import zmq
import enum
from DataKeeper import DataKeeper
from Port import Port
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

# Functions
def configure_port(ipPort, portType, connectionType, openTimeOut = False):
    context = zmq.Context()
    socket = context.socket(portType)
    if(portType == zmq.SUB):
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
    if(openTimeOut):
        socket.setsockopt(zmq.LINGER,      0)
        socket.setsockopt(zmq.AFFINITY,    1)
        socket.setsockopt(zmq.RCVTIMEO, 1000)
    if(connectionType == "connect"):
        socket.connect("tcp://" + ipPort)
    else:
        socket.bind("tcp://" + ipPort)
    return socket, context


def configure_multiple_ports(IPs , ports, portType, openTimeOut=False):
    context = zmq.Context()
    socket = context.socket(portType)
    if(portType == zmq.SUB):
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
    if(openTimeOut):
        socket.setsockopt(zmq.LINGER,      0)
        socket.setsockopt(zmq.AFFINITY,    1)
        socket.setsockopt(zmq.RCVTIMEO,  700)
    if (isinstance(IPs, list)):
        for ip in IPs:
            socket.connect("tcp://" + ip + ":" + ports)
    else:
        for port in ports:
            socket.connect("tcp://" + IPs + ":" + port)
    return socket, context

def get_ip():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


class MsgDetails(enum.Enum):
    CLIENT_DK_UPLOAD = 1
    CLIENT_DK_DOWNLOAD = 2
    MASTER_DK_REPLICATE = 3
    ######################
    CLIENT_MASTER_UPLOAD = 4
    CLIENT_MASTER_DOWNLOAD = 5
    CLIENT_MASTER_DOWNLOAD_SUCCESS = 6
    DK_MASTER_UPLOAD_SUCCESS = 7
    DK_MASTER_ALIVE = 8
    ######################
    MASTER_CLIENT_UPLOAD_DETAILS = 9
    MASTER_CLIENT_DOWNLOAD_DETAILS = 10
    ######################
    OK = 11
    FAIL = 12


class DataKeeperType(enum.Enum):
    SRC = 1
    DST = 2


# Constants #
########### Data Keepers Constants ###############
dataKeepersNum = 3
dataKeeperNumOfProcesses = 1
dataKeepersAlivePort = "30000"
dataKeepersIps = ["192.168.43.112", "192.168.43.6", "192.168.43.234"]  # TODO to be fill
dataKeeperPorts = []

########### Master Constants ###############
masterNumOfProcesses = 5
masterReplicatePort = "50001"
masterIP = "192.168.43.234"
masterPortsArr = []

########### Replcatons Constants ###############
replicationFactor = 2
replicationPeriod = 4


# Generate Ports for master processes
for i in range(50002, 50002 + masterNumOfProcesses):
    masterPortsArr.append(str(i))
    
# Generate Ports for all data keepers processes
for j in range(30002, 30002 + dataKeeperNumOfProcesses):
    dataKeeperPorts.append(str(j))

