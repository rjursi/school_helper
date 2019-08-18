from socket import *
from select import *
from time import ctime
from time import sleep
import sys
import threading
import struct
import os
from multiprocessing.pool import ThreadPool



class Server():
    

    SERVER_IP = ''
    SERVER_PORT = 12345
    BUFSIZE = 1024

    CONNECTION_LIST = []
    CLIENT_CNT = 0
    
 

    def getHostIP(self):
        # 호스트의 IP 주소만을 얻기위한 함수
        
        TestSocket = socket(AF_INET, SOCK_STREAM)
        TestSocket.connect(("gmail.com",80))
        self.SERVER_IP = str(TestSocket.getsockname()[0]) # ip 값 만을 가져옴
        # print("서버 IP : %s" % self.server_ip)
        
        TestSocket.close()

    def remote_command(self, msg):
        for socket_in_list in self.CONNECTION_LIST:
            if socket_in_list != self.CONNECTION_LIST[0]:
                
                msg = " ".join(msg)
                try:
                    socket_in_list.send(msg.encode("cp949"))

                except ConnectionResetError:
                    print("%d : 해당 클라이언트와의 연결이 끊어졌습니다." % self.CONNECTION_LIST.index(socket_in_list))
                    socket_in_list.close()
                    del self.CONNECTION_LIST[self.CONNECTION_LIST.index(socket_in_list)]
                    continue
            else:
                continue



                    
    def client_macAddr_append(self,clientMacAddr):
        try:
            macAddr_listFile = open("./client_macAddr_list.txt",'r')
            
        except FileNotFoundError:
            macAddr_listFile = open("./client_macAddr_list.txt",'w')
            macAddr_listFile.close()

            macAddr_listFile = open("./client_macAddr_list.txt",'r')


        while True:
            line = macAddr_listFile.readline().strip()
            if not line:
                break

            
            if line == clientMacAddr:
                return
            else:
                continue

        macAddr_listFile = open("./client_macAddr_list.txt",'a')
        macAddr_listFile.write(clientMacAddr + "\n")
        macAddr_listFile.close()




    def createSocketThread(self, serverSocket):


        if serverSocket:
            try:
                clientSocket, addr_info = serverSocket.accept()
            except OSError:
                return
            
            self.CONNECTION_LIST.append(clientSocket)

            self.CLIENT_CNT += 1

            newClientSockThread = threading.Thread(target = self.createSocketThread, args = (serverSocket, ))
            newClientSockThread.daemon = True
            newClientSockThread.start() 
            
            # 백그라운드 프로세스 시작
            # 백그라운드에서 다른 클라이언트가 연결 되기를 대기

            print(self.CONNECTION_LIST)
                    
            print('[INFO][%s] 클라이언트(%s) 가 연결되었습니다.' % (ctime(), addr_info[0]))
            clientMacAddr = clientSocket.recv(self.BUFSIZE).decode("cp949")

            print(clientMacAddr)

            self.client_macAddr_append(clientMacAddr)

  

    def client_connect(self, serverSocket):
        
        for sock in self.CONNECTION_LIST:
            
            if self.CLIENT_CNT == 0:


                if serverSocket:

                    try:
                        clientSocket, addr_info = serverSocket.accept()
                    except OSError:
                        return 0
                    # 연결이 되기를 기다림, 연결이 되면 다음 코드로 넘어감

                    self.CONNECTION_LIST.append(clientSocket)
                    self.CLIENT_CNT += 1


                    newClientSockThread = threading.Thread(target = self.createSocketThread, args = (serverSocket, ))
                    newClientSockThread.daemon = True
                    newClientSockThread.start() 
                    
                    # 백그라운드 프로세스 시작
                    # 백그라운드에서 다른 클라이언트가 연결 되기를 대기


                    # 공통 소켓 리스트에서 다른 클라이언트 소켓 리스트에 지속적으로 저장

                    print('[INFO][%s] 클라이언트(%s) 가 연결되었습니다.' % (ctime(), addr_info[0]))
                    clientMacAddr = clientSocket.recv(self.BUFSIZE).decode("cp949")
                
                    print(clientMacAddr)

                    self.client_macAddr_append(clientMacAddr)

                
            else: # 서버 소켓이 아닌 다른 클라이언트 소켓일 경우

                try:
                    msg = sys.stdin.readline().split()
    
                except IndexError:
                    continue
                    
                   
                    # 공백, 엔터등을 기준으로 나누어 리스트 생성, 그거의 첫번째 원소

                print(msg)

                if not msg: # 명령 리스트가 비어있으면
                    continue

                if msg[0] == "quit":
                    # print(read_socket)
                    if self.CONNECTION_LIST:
                        self.remote_command(msg)
                    elif not self.CONNECTION_LIST:
                        pass


                    # 클라이언트 단에서 먼저 종료

                    sock.close()

                    for sock in self.CONNECTION_LIST:
                        if not self.CONNECTION_LIST:
                            break   
                        else:
                            if self.CONNECTION_LIST.index(sock) != serverSocket:
                                self.CONNECTION_LIST.remove(sock)
                            else:
                                continue
                    
                    serverSocket.close()
                    del self.CONNECTION_LIST[0]
                    print("[INFO][%s] 서버의 연결이 종료되었습니다." % ctime())

                    self.CLIENT_CNT = 0
                    return 0 

                    
                if msg:
                    
                    self.remote_command(msg) 
                    continue


    def cmdServer(self):

        self.getHostIP()

        #현재 서버의 IP 수집
        

        server_ip_port = (self.SERVER_IP, self.SERVER_PORT)
        
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # 서버 소켓 객체 생성, AF_INET = IPV4, SOCK_STREAM = TCP 통신
       

        serverSocket.bind(server_ip_port)
        # 서버 IP 와 Port 할당
        
        serverSocket.listen()
    

        self.CONNECTION_LIST.append(serverSocket)
        


    
        # 클라이언트들이 연결되는 리스트

        print("====================================")
        print("서버 IP  : %s\n" % self.SERVER_IP)
        print("Port : %s\n" % self.SERVER_PORT)
        # print("quit 를 입력하면 서버 모드를 종료합니다.")
        print("접속을 기다립니다.")
        print("====================================")
        

        while self.CONNECTION_LIST:
        # 클라이언트의 응답을 계속 받을 수 있도록 무한루프로 동작
            
            quit_flag = self.client_connect(serverSocket)
            if quit_flag == 0:
                break

        
            
                


    def onOffSelect(self):
        print(('=' * 70) + "\n\n \t\t강의실 컴퓨터 On / OFF 프로그램\n\n" + ('=' * 70))
        print("수행할 작업을 선택해주세요.")
        
        print("1. 컴퓨터 ON\n2. 컴퓨터 OFF\n3. 프로그램 종료")

        optionSelect = sys.stdin.readline().strip()
        
        os.system('cls')

        return optionSelect



    
    def wolServer(self):
        
        comCount = 0

        comMacAddList = open("./client_macAddr_list.txt", 'r')

        print("컴퓨터를 킵니다.")

        while True:
            line = comMacAddList.readline().strip()
            # print(line)
            
            if not line:
                break
            
            macAddr = line.split('-')

            hw_macAddr = struct.pack("BBBBBB",int(macAddr[0],16),
            int(macAddr[1],16),int(macAddr[2],16),int(macAddr[3],16),
            int(macAddr[4],16),int(macAddr[5],16)
            )


            magicPacket = b"\xFF" * 6 + hw_macAddr * 16

            print(magicPacket)
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            sock.sendto(magicPacket, ('192.168.0.255',7))
            sock.close()

        print("모든 컴퓨터 부팅을 완료하였습니다.")

        sleep(1)

        os.system('cls')
            

if __name__ == "__main__":

    CtlServer = Server() # 서버 객체 생성

    
    while True:
        optionSelect = CtlServer.onOffSelect()


        if optionSelect == '1':
            CtlServer.wolServer()
        elif optionSelect == '2':
            CtlServer.cmdServer()
        elif optionSelect == '3':
            print("강의실 컴퓨터 제어 프로그램을 종료합니다.")
            break

    sys.exit()




    
    
