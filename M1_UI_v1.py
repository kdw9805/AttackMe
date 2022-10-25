#
#
# 해당 코드는 중부대학교 정보보호학과 '공격해조' 졸업 팀이 제작한 코드입니다.
#
#

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import M1_Code_v1
import pandas as pd
import os
from grave import plot_network
from grave.style import use_attributes


# 0. 세팅
# 아이콘 설정
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 1. 메인 UI
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.s = M1_Code_v1.ServerSocket(self)
        self.infos = None
        self.scenarioNum = 1
        self.serverstart()
        self.initUI()
        self.dialog = QDialog()

    # 통신 서버 시작
    def serverstart(self):
        self.s.start()

    # UI 기본 설정
    def initUI(self):
        # Window Size
        self.setGeometry(100, 100, 1600, 800)
        self.setWindowTitle("Attack Me v1.0.0")
        window_ico = resource_path('JBUlogo.ico')
        self.setWindowIcon(QIcon(window_ico))
        self.MeueBar()
        self.URLs()
        self.NetworkGraph()
        # Layout
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.addWidget(self.url_combo, 0, 0, 1, 1)
        grid_layout.addWidget(self.url_text, 0, 1, 1, 1)
        #grid_layout.addWidget(self.canvas, 1, 0, 2, 2)
        grid_layout.addWidget(self.url_btn, 0, 2, 1, 1)
        grid_layout.addWidget(self.canvas, 1, 0, 3, 3)
        self.setCentralWidget(grid_widget)

    # 메뉴바 설정
    def MeueBar(self):
        # MenuBar
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        # MenuBar - File Action
        self.scenario_action = QAction("Add Scenario")
        self.scenario_action.setShortcut('Ctrl+A')
        self.scenario_action.triggered.connect(self.scenarioEvent)
        self.export_action = QAction("Export CSV")
        self.export_action.setShortcut('Ctrl+E')
        self.export_action.triggered.connect(self.csvSave)
        self.quit_action = QAction("Quit")
        self.quit_action.setShortcut('Ctrl+Q')
        self.quit_action.triggered.connect(self.close)
        self.quit_action.triggered.connect(self.s.stop)
        # MenuBar - Help Action
        self.about_action = QAction("About")
        self.about_action.setShortcut('Ctrl+H')
        self.about_action.triggered.connect(self.aboutEvent)
        # MenuBar - File Menu
        file_menu = self.menubar.addMenu("File")
        file_menu.addAction(self.scenario_action)
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        # MenuBar - Help Menu
        help_menu = self.menubar.addMenu("Help")
        help_menu.addAction(self.about_action)

    # 시나리오 URL 설정
    def URLs(self):
        # URL - Combobox
        self.url_combo = QComboBox(self)
        self.url_comboList = {
            'scenario'+str(self.scenarioNum): "https://github.com/kdw9805/AttackMe/raw/main/M2_v1.py"}
        self.url_combo.setMaximumHeight(30)
        self.url_combo.addItem('None')
        self.url_combo.addItem('scenario'+str(self.scenarioNum))
        self.url_combo.activated[str].connect(self.urlEvent)
        # URL - TextBrowser
        self.url_text = QTextBrowser(self)
        self.url_text.setMaximumHeight(30)
        self.url_text.setOpenExternalLinks(True)
        self.url_text.setPlainText("scenario command")
        # URL - Button
        self.url_btn = QPushButton('run', self)
        self.url_btn.setMaximumHeight(30)
        self.url_btn.clicked.connect(self.run)


# 2. 이벤트 함수
    # 시나리오 이벤트

    def scenarioEvent(self):
        self.addurl = QLineEdit(self.dialog)
        self.addurl.move(20, 15)
        self.addurl.resize(350, 25)
        self.addbtn = QPushButton("Add", self.dialog)
        self.addbtn.move(400, 15)
        self.addbtn.clicked.connect(self.scenarioAdd)
        self.dialog.setWindowTitle('Add Scenario')
        self.dialog.resize(500, 50)
        self.dialog.show()

    # 시나리오 추가 이벤트
    def scenarioAdd(self):
        self.scenarioNum += 1
        self.url_comboList['scenario' +
                           str(self.scenarioNum)] = self.addurl.text()
        self.url_combo.addItem('scenario' +
                               str(self.scenarioNum))
        self.dialog.close()

    # 시나리오 실행 이벤트
    def run(self):
        for i in self.url_comboList.keys():
            if self.url_combo.currentText() == i:
                cmd = 'powershell.exe -command "invoke-WebRequest {} -Outfile C:\AttackMe\download\M2_v1.py"; python "C:\AttackMe\download\M2_v1.py'.format(
                    self.url_comboList[i])
                print(cmd)
                os.system(cmd)

    # CSV 이벤트
    def csvSave(self):
        csv_Name = []
        csv_IP = []
        csv_Port = []
        csv_Info = []
        for node in self.G.nodes:
            csv_Name.append(self.G.nodes[node]['name'])
            csv_IP.append(self.G.nodes[node]['ip'])
            csv_Port.append(self.G.nodes[node]['port'])
            csv_Info.append(self.G.nodes[node]['infos'])
        df = pd.DataFrame(csv_Name, columns=['name'])
        df['ip'] = csv_IP
        df['port'] = csv_Port
        df['infos'] = csv_Info
        df.to_csv("info.csv", index=False)
        reply = QMessageBox.question(self, 'CSV 파일 생성 완료', 'CSV 파일 생성이 완료 되었습니다.',
                                     QMessageBox.Yes, QMessageBox.Yes)

    # 어바웃 이벤트
    def aboutEvent(self):
        reply = QMessageBox.question(self, 'Attack Me', 'Attack Me v1.0.0\n[developer]\n김진수: have2429@gmail.com\n오원재: oh1j0511@gmail.com\n여수한: tkdldjs986@gmail.com\n김대원: nokka4860@gmail.com',
                                     QMessageBox.Yes, QMessageBox.Yes)

    # URL 이벤트
    def urlEvent(self):
        for i in self.url_comboList.keys():
            print(i)
            if self.url_combo.currentText() == i:
                html = self.url_comboList[i]
                self.url_text.setHtml(html)


# 3. 네트워크 그래프
    # 기본 네트워크 그래프 설정

    def NetworkGraph(self):
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.fig.clf()
        self.G = nx.Graph()
        self.G.add_node('DC', name='DC', ip='xxx.xxx.xxx.xxx', port='None')
        nx.draw(self.G, with_labels=True, node_size=1000)
        self.canvas.draw_idle()

    # 통신된 모듈 노드 추가
    def updateClient(self, port, m_dict, isConnect=False):
        nodes = self.G.nodes()
        print('nodes: ', nodes)
        if isConnect:
            try:
                self.G.nodes[m_dict['NAME']]
                if self.G.nodes[m_dict['NAME']]['infos'] is not None:
                    self.G.nodes[m_dict['NAME']]['infos'] = self.G.nodes[m_dict['NAME']
                                                                         ]['infos'] + m_dict['INFO']
                else:
                    self.G.nodes[m_dict['NAME']]['infos'] = m_dict['INFO']
            except:
                self.G.add_node(m_dict['NAME'], name=m_dict['NAME'], ip=m_dict['IP'],
                                port=port[1], infos=m_dict['INFO'])
            nx.add_star(self.G, nodes)
            plt.clf()
            for node in self.G.nodes:
                self.G.nodes[node]['size'] = 1000
            self.art = plot_network(self.G, node_style=use_attributes(), node_label_style={
                                    'font_size': 10, 'font_backgroundcolor': None})
            self.art.set_picker(10)
            self.fig.canvas.mpl_connect('pick_event', self.hilighter)
            self.canvas.draw_idle()
        else:
            pass

    # 선택된 노드 강조
    def hilighter(self, event):
        if not hasattr(event, 'nodes') or not event.nodes:
            return
        for node, attributes in self.G.nodes.data():
            attributes.pop('color', None)
        for node in event.nodes:
            self.G.nodes[node]['color'] = 'C1'
            reply = QMessageBox.question(self, '%s' % self.G.nodes[node]['name'], 'IP: %s   Port: %s\nInfo:\n%s' % (
                self.G.nodes[node]['ip'], self.G.nodes[node]['port'], self.G.nodes[node]['infos']), QMessageBox.Yes, QMessageBox.Yes)
        event.artist.stale = True
        event.artist.figure.canvas.draw_idle()


# 4. Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
