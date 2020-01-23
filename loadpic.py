import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import visa
import string
import struct
import requests
import screenshotsave
from measurev import do_command, do_query_string,do_query_number

debug = 0

rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll')
InfiniiVision = rm.open_resource("USB0::0x0957::0x179B::MY51452776::0::INSTR")
InfiniiVision.timeout = 15000
InfiniiVision.clear()

############################################################
#数据测试与读取
############################################################
do_command(":MEASure:VMAX")
qresult_vmax = do_query_number(":MEASure:VMAX?")

do_command(":MEASure:VMIN")
qresult_vmin = do_query_number(":MEASure:VMIN?")

do_command(":MEASure:VPP")
qresult_vpp = do_query_number(":MEASure:VPP?")

do_command(":MEASure:VAVerage")
qresult_vav = do_query_number(":MEASure:VAVerage?")

do_command(":MEASure:FREQuency")
qresult_fre = do_query_number(":MEASure:FREQuency?")

do_command(":MEASure:PERiod")
qresult_per = do_query_number(":MEASure:PERiod?")


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super(TextEditDemo, self).__init__(parent)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        self.setWindowTitle('Measure')
        self.setGeometry(50, 50, 1000, 800)
        btnPress1 = QPushButton('显示测量数据')
        btnPress1_half_1 = QPushButton('Single')
        btnPress1_half_2 = QPushButton('STOP')
        btnPress1_half_3 = QPushButton('RUN')
        btnPress2 = QPushButton('AUTO控制键')
        btnPress3 = QPushButton('退出Qt界面')

        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        splitter_run_and_stop = QSplitter(Qt.Horizontal)
        splitter_run_and_stop.addWidget(btnPress1_half_3)
        splitter_run_and_stop.addWidget(btnPress1_half_2)

        splitter1_half = QSplitter(Qt.Vertical)
        splitter1_half.addWidget(btnPress1)
        splitter1_half.addWidget(btnPress1_half_1)
        splitter1_half.addWidget(splitter_run_and_stop)

        splitter1 = QSplitter(Qt.Horizontal)
        self.textedit = QTextEdit()
        splitter1.addWidget(splitter1_half)
        splitter1.addWidget(self.textedit)
        splitter1.setSizes([100, 300])

        splitter2_half = QSplitter(Qt.Horizontal)
        splitter2_half.addWidget(btnPress2)
        splitter2_half.addWidget(btnPress3)

        label1 = QLabel(self)
        label1.setPixmap(QPixmap("D:\\DATA\\Scope_Image.png"))
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)

        splitter2_assemble = QSplitter(Qt.Vertical)
        splitter2_assemble.addWidget(label1)
        splitter2_assemble.addWidget(splitter2_half)
        splitter2_assemble.setSizes([300, 100])
        # splitter2.addWidget(bottom)
        splitter2.addWidget(splitter2_assemble)
        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        # 将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        btnPress1.clicked.connect(self.btnPress1_clicked)
        btnPress2.clicked.connect(self.btnPress2_clicked)
        btnPress3.clicked.connect(self.close)
        btnPress1_half_1.clicked.connect(self.btnPress1_half_1_clicked)
        btnPress1_half_2.clicked.connect(self.btnPress1_half_2_clicked)
        btnPress1_half_3.clicked.connect(self.btnPress1_half_3_clicked)

    def btnPress1_clicked(self):
        # 以文本的形式输出到多行文本框
        self.textedit.setPlainText(
            "VMAX(伏特) : %s\nVMIN(伏特) : %s\nVPP(伏特) : %s\nV average(伏特) : %s\nFrequency(赫兹) : %s\nPeriod(秒) : %s\n" % (
            qresult_vmax, qresult_vmin, qresult_vpp, qresult_vav, qresult_fre, qresult_per))

    def btnPress2_clicked(self):
        do_command(":AUToscale")
        # 控制AUTO键

    def btnPress1_half_1_clicked(self):
        do_command(":SINGle")

        # 控制垂直调整旋钮

    def btnPress1_half_2_clicked(self):
        do_command(":STOP")
        # 控制水平调整旋钮

    def btnPress1_half_3_clicked(self):
        do_command(":RUN")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())