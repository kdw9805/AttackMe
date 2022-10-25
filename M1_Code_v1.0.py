#
#
# 해당 코드는 중부대학교 정보보호학과 '공격해조' 졸업 팀이 제작한 코드입니다.
#
#

from threading import Thread
import socket
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import json


# 1. Main
class ServerSocket(QObject):
    update_signal = pyqtSignal(tuple, dict, bool)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.Module_BoolListen = False
        self.Module_Clients = []
        self.Module_Names = []
        self.Module_IPs = []
        self.info_List = []
        self.update_signal.connect(self.parent.updateClient)

    def __del__(self):
        self.stop()

    def start(self):
        Host = '192.168.0.133'
        Port = 9999
        self.server = socket(AF_INET, SOCK_STREAM)
        try:
            self.server.bind((Host, Port))
        except Exception as e:
            print('Bind Error:', e)
            return False
        else:
            self.Module_BoolListen = True
            self.Module_Thread = Thread(
                target=self.listen, args=(self.server,))
            self.Module_Thread.start()
        return True

    def stop(self):
        self.Module_BoolListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server Stop')

    def listen(self, server):
        while self.Module_BoolListen:
            server.listen(5)
            try:
                Module_Client, Server_IP = server.accept()
                m_dict = Module_Client.recv(1024)
                m_dict = json.loads(m_dict)
            except Exception as e:
                print('Accept() Error', e)
                break
            else:
                self.Module_Clients.append(Module_Client)
                self.Module_IPs.append(m_dict['IP'])
                self.Module_Names.append(m_dict['NAME'])
                self.update_signal.emit(Server_IP, m_dict, True)
                Module_Thread = Thread(
                    target=self.recive, args=(Module_Client, m_dict))
                Module_Thread.start()
        # self.removeAllClients(m_dict)
        self.server.close()

    def recive(self, Module_Client, m_dict):
        while True:
            try:
                recv = Module_Client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = recv.decode('ascii')
                if msg == 'OK':
                    Module_Client.send('OK'.encode('ascii'))
                    break
        self.removeClient(Module_Client, m_dict)

    def removeClient(self, Module_Client, m_dict):
        Module_Client.close()
        self.Module_IPs.remove(m_dict['IP'])
        self.Module_Clients.remove(Module_Client)
        self.Module_Names.remove(m_dict['NAME'])
        self.update_signal.emit(Module_Client, m_dict, False)

    def removeAllClients(self, m_dict):
        for Module_Client in self.Module_Clients:
            Module_Client.close()
        for Module_IP in self.Module_IPs:
            self.update_signal.emit(m_dict, False)
        self.Module_IPs.clear()
        self.Module_Clients.clear()
