'''
Created on Feb 14, 2019

@author: reynolds
'''

import sys

from PyQt5.QtWidgets import QApplication,QMainWindow, QPushButton, QGridLayout,\
    QWidget
from wrtdk.instrument.fieldfox.N9918A import N9918A
from wrtdk.comms.comms import SerialPort
from wrtdk.io.streamer.vnastreamer import fieldfox_streamer

class test(QMainWindow):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Constructor '''
        QMainWindow.__init__(self)
        
        main = QWidget(self)
        btn = QPushButton('Connect')
        btn.clicked.connect(self._connect)
        log = QPushButton('Log')
        log.clicked.connect(self._log)
        
        l = QGridLayout()
        l.addWidget(btn)
        l.addWidget(log)
        
        main.setLayout(l)
        self.setFocus()
        self.setCentralWidget(main)
        
        self._port = None
        self._thread = None
        
    def _connect(self):
        if self._port is None:
            self._port = []
            self._port.append(N9918A(dict(verb=True,
                                          addr='128.128.204.202',
                                          trans='OFF',
                                          form='POL',
                                          timeout=2000,
                                          chunk_size=102400,
                                          dform='REAL,64',
                                          np=401,
                                          spwr=-1.6)))
            self._port.append(SerialPort('COM8',9600))
            self._thread = fieldfox_streamer(self._port)
            self._thread.start()
        else:
            self._thread.stop()
            self._thread.wait()
            self._thread = None
            self._port = None
            
    def _log(self):
        if self._thread.isRunning():
            print(self._thread.isLogging())
            if self._thread.isLogging():
                self._thread.stopLog()
            else:
                self._thread.startLog('test.csv')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    aw = test()
    aw.show()
    app.exec_()