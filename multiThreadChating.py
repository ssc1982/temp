#encoding=utf-8

import socket
import threading

threadLocal = threading.local().

#receive data from server
def recvData():

    while True:
        data, addr = udpSocket.recvfrom(1024)
        print("Server end %s says#: %s" % (addr, data))

#send message to server
def sendData():

    while True:
        servIP = input("please enter the server IP:")
        servPort = int(input("please enter the server port:"))
        data = input("date you wanna send:")

        udpSocket.sendto(data.encode("gb2312"), (servIP, servPort))

#main control function
def main():

    global udpSocket
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind(("", 8888))

    r_thrd = threading.Thread(target=recvData)
    s_thrd = threading.Thread(target=sendData)

    r_thrd.start()
    s_thrd.start()

    r_thrd.join()
    s_thrd.join()


if __name__ == '__main__':
    main()