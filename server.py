import socket
import sys

class Server:
    server_ip = ''
    server_info = []
    
    def ServerInfoSave(self):
        ServerInfo = open("./ServerInfo.txt",'w+')

        for data in self.server_info:
            ServerInfo.write(str(data) + ' ')
        ServerInfo.close()
            

    def getHostIP(self):
        # 호스트의 IP 주소만을 얻기위한 함수
        
        TestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TestSocket.connect(("gmail.com",80))
        self.server_ip = str(TestSocket.getsockname()[0]) # ip 값 만을 가져옴
        print("서버 IP : %s" % self.server_ip)
        
        TestSocket.close()

    def send_command(self, serverSocket, connectionSocket):
        while True:
            cmd = input()
            if cmd == 'quit':
                connectionSocket.close()
                serverSocket.close()
                sys.exit()

                # quit 명령이 들어오면 세션 종료
                
            if len(str.encode(cmd)) > 0:
                connectionSocket.send(str.encode(cmd))
                client_response = connectionSocket.recv(2048)
                print(client_response)
                client_response = str(client_response.decode("cp949"))
                # 클라이언트로부터 받은 메세지를 변수에 저장

                print(client_response, end="")
                
                # 클라이언트에서 실행한 명령의 결과를 서버측에서도 확인하기 위하여 출력


    def runServer(self):

        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print("socket creation error: " + str(msg))

        self.getHostIP()

        #현재 서버의 IP 수집
        #서버 소켓 객체 생성, AF_INET = IPV4, SOCK_STREAM = TCP 통신
        try:
            serverSocket.bind((self.server_ip,0))   
        except socket.error as msg:
            print("Socket binding error : " + str(msg) + "\n" + "Retrying.....")
            serverSocket.socket_bind()

        for data in serverSocket.getsockname():
            self.server_info.append(data)
        
        # ip 주소와 port 번호를 server_info 클래스 리스트 변수에 저장

        self.server_info = tuple(self.server_info)
        
        self.ServerInfoSave()


        # 클라이언트에게 서버 IP와 포트값 넘기기 위해 모듈 사용

        #bind 는 서버 소켓과 AF를 연결하는 과정,'' = INADDR_ANY, 어떤 IP 든 받는다.
        #0의미는 해당 호스트에서 확인을 하여 랜덤으로 포트를 할당을 한다.
        #목록을 튜플로 할당

        serverSocket.listen(50)
        #총 50개의 동시접속자까지 허용을 한다.

        

        connectionSocket, addr = serverSocket.accept()
        # accept() : 소켓에 누군가가 접속하여 연결되었을때 결과값이 return 되는 함수, 클라이언트와 서버의 연결이 성립이 될 경우 
        #            값을 반환

        # connectionSocket 에는 클라이언트로부터 데이터를 받을 객체를 생성, 초기값으로 서버에 대한 주소와 포트(laddr), 클라이언트의 주소 및 포트 정보(raddr)가 들어가있음


        print(str(addr[0]), '에서 접속이 확인되었습니다.')
        #print(str(connectionSocket))

        self.send_command(serverSocket,connectionSocket)
        
if __name__ == "__main__":
    CtlServer = Server() # 서버 객체 생성
    CtlServer.runServer()
    
