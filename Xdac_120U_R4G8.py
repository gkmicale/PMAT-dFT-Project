
import zmq
import time
import csv
import numpy as np

from time import sleep

##
##=========================================================
##

# Change with XDAC IP Address
XDAC_IP = "192.168.18.159"

# Connect to Req Server on XDAC via ZMQ
context = zmq.Context()
req_socket = context.socket(zmq.REQ)
req_socket.connect("tcp://%s:5555" % XDAC_IP)

sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://%s:5556" % XDAC_IP)

subV_socket = context.socket(zmq.SUB)
subV_socket.connect("tcp://%s:5556" % XDAC_IP)

subC_socket = context.socket(zmq.SUB)
subC_socket.connect("tcp://%s:5556" % XDAC_IP)


# edit channel maximum of Xpow
channelMax = 120

# default range array for all channel
channelRange = [3] * channelMax

# Range Dictionary
RANGE_DICT = {
    0: (0, 5),
    1: (0, 10),
    2: (0, 20),
    3: (0, 40)
}

def unlock(key):

    #Send Request to XDAC (Server)
    msg = "GETINFO:" + key
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()

    return (message.decode('utf-8')) 

def lock():

    #Send Request to XDAC (Server)
    msg = "LOCK"
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()

    return (message.decode('utf-8')) 

def shutdown():

    #Send Request to XDAC (Server)
    msg = "EXIT"
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()

    return (message.decode('utf-8')) 


# setChannel: set voltage of each channel
# setChannelVoltage(ch, voltage (in V))
def setChannelVoltage(channel, voltageVal):

    if channel > channelMax:
        print("Channel exceeds the limit")
        return 1

    #Set threeshold fo Current and Voltage    
    MinVoltage, MaxVoltage = RANGE_DICT[channelRange[channel-1]]
    
    if voltageVal > MaxVoltage:
        voltageVal = MaxVoltage
    elif voltageVal < MinVoltage:
        voltageVal = MinVoltage

    #Send Request to XDAC (Server)
    msgV = "SETV:" + ("%d" % channel) + ":" + ("%.3f" % voltageVal)
    req_socket.send(msgV.encode('utf-8'))
    message = req_socket.recv()
        
    return 0

# setChannel: set voltage of each channel
# setChannelVoltage(ch, voltageByte (in int value 0-65535 (@ 0 - Voltage Range (40V = default, use setChannelVoltageRange() to change the range))))
def setChannelVoltageByte(channel, voltageByte):

    if channel > channelMax:
        print("Channel exceeds the limit")
        return 1

    #Send Request to XDAC (Server)
    msgV = "BITV:" + ("%d" % channel) + ":" + ("%d" % voltageByte)
    req_socket.send(msgV.encode('utf-8'))
    message = req_socket.recv()
        
    return 0

# setChannel: set current of each channel
# setChannelCurrent(ch, current (in mA))
def setChannelCurrent(channel, currentVal):

    if channel > channelMax:
        print("Channel exceeds the limit")
        return 1

    #Set threeshold fo Current and Voltage    
    MaxCurrent = 300

    if currentVal > MaxCurrent:
        voltageVal = MaxCurrent
    elif currentVal < 0.0:
        currentVal = 0.0

    #Send Request to XDAC (Server)
    msgC = "SETC:" + ("%d" % channel) + ":" + ("%.3f" % currentVal)
    req_socket.send(msgC.encode('utf-8'))
    message = req_socket.recv()
        
    return 0

# setChannel: set current of each channel
# setChannelCurrent(ch, current (in int value, 0-65535 (@ 0-300mA)))
def setChannelCurrentByte(channel, currentByte):

    if channel > channelMax:
        print("Channel exceeds the limit")
        return 1

    #Send Request to XDAC (Server)
    msgC = "BITC:" + ("%d" % channel) + ":" + ("%d" % currentByte)
    req_socket.send(msgC.encode('utf-8'))
    message = req_socket.recv()
        
    return 0

# setChannel: set voltage of each channel
# setChannelVoltage(ch, voltage (in V))
def setChannelVoltageRange(channel, _range):

    if channel > channelMax:
        print("Channel exceeds the limit")
        return 1

    if _range not in range(4,8):
        print("Wrong Channel Range, please look at Range Dictionary")
        return 1

    channelRange[channel-1] = _range 

    #Send Request to XDAC (Server)
    msg = "SETR:" + ("%d" % channel) + ":" + str(_range)
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()

    return 0

# setVoltageAllChannels: set voltage of all channels
# AllVValues = [8, 8, -1, 2, 3, 4, 5, 7] for 8 Channels
# setVoltageAllChannels(AllVValues)
def setVoltageAllChannels(AllVValues):

    msg = "SETMULTIA;:" + ":".join([f"V{x+1}:{y:.3f}" for x,y in enumerate(AllVValues)]) + ";"
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()
     
    return 0

# setCurrentAllChannels: set current of all channels
# AllCValues = [200, 200, 300, 50, 300, 400, 450, 250] for 8 Channels
# setCurrentAllChannels(AllCValues)
def setCurrentAllChannels(AllCValues):

    msg = "SETMULTIA;;:" + ":".join([f"C{x + 1}:{y:.3f}" for x, y in enumerate(AllCValues)])
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()
     
    return 0

# setRangeAllChannels: set voltage range of all channels
# AllRValues = [5, 5, 5, 5, 5, 5, 5, 5] for 8 Channels
# setCurrentAllChannels(AllCValues)
def setRangeAllChannels(AllRValues):

    for channel, value in enumerate(AllRValues):
        channel = channel + 1 #Channel start from 1
        setChannelVoltageRange(channel, value)

    return 

def setOffAllChannel():

    #Send Request to XDAC (Server)
    msg = "ZERO:ALL"
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()   

    return 0

# setOff:  set one channel to zero
# setOff(1) -> set 0 V, 0 mA, to channel 1.
def setOff(channel):

    #Channel Validation
    if channel > channelMax:
        print("Channel exceeds the limit")
        return 1

    #Send Request to XDAC (Server)
    msg = "ZERO:" + ("%d" % channel)
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()   

    return 0

# readSingleChannelCurrent: Read single channel current 
# current = readSingleChannelCurrent(1) -> read current for channel 1
def readSingleChannelCurrent(channel):

    #Send Request to XDAC (Server)
    msg = "MEASC:" + ("%d" % channel)
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()

    return (message.decode('utf-8'))

# readSingleChannelVoltage: Read single channel Voltage 
# voltage = readSingleChannelVoltage(1) -> read Voltage for channel 1
def readSingleChannelVoltage(channel):

    #Send Request to XDAC (Server)
    msg = "MEASV:" + ("%d" % channel)
    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()

    return (message.decode('utf-8'))

# readAllChannelsCurrent: Read All channel current 
def readAllChannelsCurrent():

    subC_socket.setsockopt(zmq.SUBSCRIBE, b'C')

    string = subC_socket.recv()
    # print(string)
    msg = string.decode('utf-8')
    value = msg[1:-1].split(",")

    return value[0:-1:2]


# readAllChannelCurrent: Read All channel current 
def readAllChannelsVoltage():

    subV_socket.setsockopt(zmq.SUBSCRIBE, b'V')

    string = subV_socket.recv()
    # print(string)
    msg = string.decode('utf-8')
    value = msg[1:-1].split(",")

    return value[0:-1:2]

def measurementConfig(averagingSample, voltageConv, currentConv):
    
    #Send Request to XDAC (Server)
    msg = ("CONFIG:" +
           str(averagingSample) + ":" +
           str(voltageConv) + ":" +
           str(currentConv))

    req_socket.send(msg.encode('utf-8'))
    message = req_socket.recv()   

    return 0

# set one channel to run automatically and record it.
# duration in seconds
# example:
# seqValueV = [1, 2, 3, 4, 5, 6, 7, 8]
# seqValueC = [10, 10, 10, 10, 10, 10, 10, 10]
# sweepOne (1, seqValueV, seqValueC, 5)
# set channel 1 to change voltage value based on seqValueV and current value based seqValueC, for every 5 seconds
def sweepOne(channel, seqValueV, seqValueC, duration):
    
    readValueV = []
    readValueC = []  
    for valuev, valuec in zip(seqValueV, seqValueC):
        setChannelVoltage(channel, valuev)
        setChannelCurrent(channel, valuec)
        sleep(duration)
        readValueV.append(readSingleChannelVoltage(channel))
        readValueC.append(readSingleChannelCurrent(channel))
        
    with open('data AA.csv', mode='w') as csv_file:
        fieldnames = ['setV(v)', 'voltage(v)', 'current(mA)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for value in range(len(readValueV)):
            writer.writerow({'setV(v)': seqValueV[value], 'voltage(v)': float(readValueV[value]), 'current(mA)': readValueC[value]})

    print("function end")

    return



# Edit input voltage with value from -20 - 20 V
# Example: InputV = [1, 2, 3, 4, 5, 6, 7, 8]
# Edit InputV to set the voltage of each channel
# InputV = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 12
InputV = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 12

# Edit input current with value from 0 - 500 mA
# Example:InputC = [5, 10, 50, 100, 150, 200, 250, 300]
# Edit InputC to set the current of each channel
InputC = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100] * 12
 
# Edit input range with value from 4 - 7
# Example:InputC = [5, 5, 5, 5, 5, 5, 5, 5]
# Edit InputC to set the current of each channel
InputR = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3] * 12 


print(unlock("nicslab"))

# Set measurement averaging sample and conversion time
# averaging sample = 1
# Voltage Conversion Time = 588 uS
# Current Conversion Time = 588 uS
# measurementConfig(1,588,588)

# averaging sample = 16
# Voltage Conversion Time = 144 uS
# Current Conversion Time = 144 uS
# measurementConfig(16, 144, 144)

# Example Code 1 -----------------------------------------------------------------------

# setVoltageAllChannels(InputV)
# setCurrentAllChannels(InputC)
# time.sleep(0.05)
# print(readAllChannelsVoltage())
# print(readAllChannelsCurrent())

# Example Code 1 - end  ----------------------------------------------------------------

# Example Code 2 -----------------------------------------------------------------------

# set channel 1 with -5 V and 150 mA

# setChannelVoltage(1, 5)
# setChannelCurrent(1, 200)
# time.sleep(0.5)
# print(readSingleChannelVoltage(1),readSingleChannelCurrent(1))

# setChannelVoltage(1, 3)
# setChannelCurrent(1, 300)
# time.sleep(0.5)
# print(readSingleChannelVoltage(1),readSingleChannelCurrent(1))
# setOff(1)

# Example Code 2 - end  ----------------------------------------------------------------

# Example Code 3 -----------------------------------------------------------------------

# channel = 120
# seqValueV = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
# seqValueC = [300, 300, 300, 300, 300, 300, 300, 300, 300, 300]
# duration = 1
# sweepOne(channel, seqValueV, seqValueC, duration)
# setOff(channel)

# Example Code 3 - end  ----------------------------------------------------------------

lock()
#shutdown()