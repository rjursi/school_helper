from socket import *
from select import *
from time import ctime
import sys


class Server:
    SERVER_IP = ''
    SERVER_PORT = 12345
    BUFSIZE = 1024


    def getHostIP(self):
        # 호스트의 IP 주소만을 얻기위한 함수
        
        TestSocket = socket(AF_INET, SOCK_STREAM)
        TestSocket.connect(("gmail.com",80))
        self.SERVER_IP = str(TestSocket.getsockname()[0]) # ip 값 만을 가져옴
        # print("서버 IP : %s" % self.server_ip)
        
        TestSocket.close()

    def remote_command(self, msg, read_socket, serverSocket):
        for socket_in_list in read_socket:
            if socket_in_list != serverSocket:
                
                msg = " ".join(msg)
                try:
                    socket_in_list.send(msg.encode("cp949"))

                except ConnectionResetError:
                    print("%d : 해당 클라이언트와의 연결이 끊어졌습니다." % read_socket.index(socket_in_list))
                    socket_in_list.close()
                    del read_socket[1]
                    continue


                    
    def client_macAddr_append(self,clientMacAddr):
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


    def client_connect(self, read_socket, serverSocket):

        print(read_socket)
        for sock in read_socket:
            if sock == serverSocket:
                clientSocket, addr_info = serverSocket.accept()
                read_socket.append(clientSocket)
                
                print('[INFO][%s] 클라이언트(%s) 가 연결되었습니다.' % (ctime(), addr_info[0]))
                clientMacAddr = clientSocket.recv(self.BUFSIZE).decode("cp949")
        
                print(clientMacAddr)

                self.client_macAddr_append(clientMacAddr)
                continue
            
                # 리스트에서 소켓 리스트를 읽음, 그러나 serverSocket밖에 없다면 clientSocket를 새로 추가함
                
                
                
            else:
                while True:
                    try:
                        msg = sys.stdin.readline().split()
                    except IndexError:
                        continue
                    
                    # print(msg)
                    # 공백, 엔터등을 기준으로 나누어 리스트 생성, 그거의 첫번째 원소

                    if not msg: # 명령 리스트가 비어있으면
                        continue

                    if msg[0] == "quit":
                        # print(read_socket)
                        if read_socket:
                            self.remote_command(msg, read_socket, serverSocket)
                        elif not read_socket:
                            pass


                        # 클라이언트 단에서 먼저 종료


                        sock.close()
                        for sock in read_socket:
                            if not read_socket:
                                break   
                            else:
                                read_socket.remove(sock)
                        
                        serverSocket.close()
                        print("[INFO][%s] 서버의 연결이 종료되었습니다." % ctime())
                        sys.exit()
                        
                    

                    if msg:
                        
                        self.remote_command(msg, read_socket, serverSocket) 
                        continue
                    
        
    def __init__(self):
        
        self.getHostIP()

        #현재 서버의 IP 수집
        

        server_ip_port = (self.SERVER_IP, self.SERVER_PORT)
        
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # 서버 소켓 객체 생성, AF_INET = IPV4, SOCK_STREAM = TCP 통신
       

        serverSocket.bind(server_ip_port)
        # 서버 IP 와 Port 할당
        
        serverSocket.listen(50)
        
        # 50개의 호스트의 요청을 기다림

        connection_list = [serverSocket]
    
        # 클라이언트들이 연결되는 리스트

        print("====================================")
        print("서버 IP  : %s\n" % self.SERVER_IP)
        print("Port : %s\n" % self.SERVER_PORT)
        print("접속을 기다립니다.")
        print("====================================")
        
        while connection_list:
        # 클라이언트의 응답을 계속 받을 수 있도록 무한루프로 동작
        
            try:
                
                read_socket, write_socket, error_socket = select(connection_list, [], [], 10)
                # select 로 요청을 받고, 10초마다 블럭킹을 해제하도록 함
                # I/O 다중화 구현할 때 select 이용

                # 즉 10초마다 다른 소켓에 클라이언트가 접속이 되었는지 체크하는 것을 말함

                # select 함수에서 자체적으로 3개의 값을 return 을 하며, 각각 3개의 소켓을 반환함
                # connection_list 를 매개변수로 넣었는데, 여기 리스트에 있는 소켓중 하나에 접속이 발생할때까지 대기
                # 접속이 되기 전까지는 block 상태
                # 클라이언트가 접속할 때에만 각 클라이언트에 적합한 작업을 수행

                self.client_connect(read_socket, serverSocket)


            except KeyboardInterrupt:
                print("Ctrl + C 입력으로 인한 종료")
                serverSocket.close()

                sys.exit()
                 
if __name__ == "__main__":

    CtlServer = Server() # 서버 객체 생성
   
    
