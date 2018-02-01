#encoding=utf-8

import struct
import socket
import os
import time
servIP = "192.168.0.112"
servPort = 69
fileName = b"01-wireshark.flv"
fileFlag = 0

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind(("", 8888))

def create_connection():
    global s_time
    requestMsg = struct.pack("!H%dsb5sb"%len(fileName), 1, fileName, 0, b"octet", 0)
    udpSocket.sendto(requestMsg, (servIP, servPort))
    s_time = time.time()
    print("Sending request to establish connection with tftp server: %s" % servIP)

def messageHandler():
    global fileFlag
    while True:
        #receive response from server
        recvData, serverInfo = udpSocket.recvfrom(1024)
        operBits, blockNum = struct.unpack("!HH", recvData[:4])
        if operBits == 3:
            print("Block number %0.3d has been received" % blockNum)
            if os.path.isfile(fileName) and fileFlag == 0:
                os.remove(fileName)
            else:
                with open(fileName, "ab") as f:
                    f.write(recvData[4:])
                    fileFlag = 1
            # acknowledge to server
            ackMsg = struct.pack("!HH", 4, blockNum)
            #print(ackMsg)
            udpSocket.sendto(ackMsg, serverInfo)
        elif operBits == 5:
            print("Error has occured, Error code:%d ==> Reason: %s " % (blockNum, recvData[:4]))
            break
        if len(recvData[4:]) < 512:
            global s_time
            print("Download complete")
            e_time = time.time() - s_time
            print("it takes %s seconds to download" % e_time)
            break

if __name__ == '__main__':
    # create connection with tftp server
    create_connection()
    # handle messages with server
    messageHandler()
