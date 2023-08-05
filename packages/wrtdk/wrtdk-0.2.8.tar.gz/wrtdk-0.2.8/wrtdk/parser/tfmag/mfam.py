'''
Created on Aug 17, 2018

@author: reynolds
'''

import os, sys, struct
from wrtdk.parser.parser import parser
from wrtdk.parser.msg.wrtmsg import udp_wrapper

class mx3g(parser):
    ''' parser for the mfam mx3g message type'''

    def __init__(self):
        ''' Constructor '''
        super().__init__()# inherit superclass
        
        # initialize properites
        self.reset()
        
        # define constants
        self.COUNT_2_NT_VMAG = 1#1000 / 75
        self.COUNT_2_DEG_C = 1
        self.COUNT_2_NT = 50e-6
        
    def reset(self):
        ''' resets the parser '''
        self._pps = self._minus1()
        self._synch = self._minus1()
        self._failed = self._minus1()
        self._id = self._minus1()
        self._count = self._minus1()
        self._status1 = self._minus1()
        self._status2 = self._minus1()
        self._mag1 = self._nan()
        self._stat1 = self._minus1()
        self._mag2 = self._nan()
        self._stat2 = self._minus1()
        self._bx = self._nan()
        self._by = self._nan()
        self._bz = self._nan()
        self._temperature = self._nan()
        self._checksum = self._minus1()
    
    def parse(self,msg):
        ''' parses the messages from the mx3g sensor platform '''
        self.reset()
        try:
            fid,stat,self._mag1,stat1,stat2,self._mag2,self._bx,self._by,self._bz,self._temperature,_ = struct.unpack('>HHihhihhhhi',msg)
            self._id = ((fid >> 8) & 0xf8)
            self._count = (fid & 0xff) + (((fid >> 8) & 0x07) << 8)
            self._pps = ((stat & 0xff) & 0b10000000) >> 7
            self._synch = ((stat & 0xff) & 0b01000000) >> 6
            self._failed = ((stat >> 8) & 0b00000001)
            self._mag1  *= self.COUNT_2_NT
            self._status1 = (stat1 & 0xE0) >> 5
            self._status2 = (stat2 & 0xE0) >> 5
            self._mag2 *= self.COUNT_2_NT
            self._bx *= self.COUNT_2_NT_VMAG
            self._by *= self.COUNT_2_NT_VMAG
            self._bz *= self.COUNT_2_NT_VMAG
            self._temperature *= self.COUNT_2_DEG_C
            self._checksum = self._calculateChecksum(msg)
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))
            
    def getData(self):
        ''' returns the data from the message 
        0) mag 1 total field in nT
        1) mag 2 total field in nT
        2) bx in nT
        3) by in nT
        4) bz in nT
        5) temperature in F
        6) mag1 status
        7) mag2 status
        8) id bits
        9) count
        10) pps flag
        11) synched flag
        12) failed flag'''
        return [self._mag1,self._mag2,
                self._bx,self._by,self._bz,
                self._temperature,
                self._status1,self._status2,
                self._id,self._count,self._pps,self._synch,self._failed]
    
    def debug(self):
        ''' debugs the message '''
        return 'id:%4d n:%4d m1:%10.3f s1:%2d s2:%2d m2:%10.3f' % (self._id,
                                                                   self._count,
                                                                   self._mag1,
                                                                   self._status1,
                                                                   self._status2,
                                                                   self._mag2)
    
class mfamfile(mx3g):
    ''' parses the mfam messages from a file '''
    
    def __init__(self):
        ''' Constructor '''
        super().__init__()# inherit superclass
    
    def parse(self, msg):
        ''' little endian parser '''
        
        try:
            fid,stat,self._mag1,stat1,stat2,self._mag2,self._bx,self._by,self._bz,self._temperature,_ = struct.unpack('<HHihhihhhhi',msg)
            self._id = (0b11111000 & (fid)) >> 3
            self._count = (fid >> 8) & 0xff + ((fid & 0b00000111) << 8)
            self._pps = ((stat & 0xff) & 0b10000000) >> 7
            self._synch = ((stat & 0xff) & 0b01000000) >> 6
            self._failed = ((stat >> 8) & 0b00000001)
            self._mag1 *= self.COUNT_2_NT
            self._status1 = stat1#(stat1 & 0b11100000) >> 5
            self._status2 = stat2#(stat2 & 0b11100000) >> 5
            self._mag2 *= self.COUNT_2_NT
            self._bx *= self.COUNT_2_NT_VMAG
            self._by *= self.COUNT_2_NT_VMAG
            self._bz *= self.COUNT_2_NT_VMAG
            self._temperature *= self.COUNT_2_DEG_C
            self._checksum = self._calculateChecksum(msg)
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))

def test_mfamfile():
    print('testing mfamfile ...')
    tf = mfamfile()
    filename = r'C:\Users\reynolds\Documents\1704_madunit\data\20180830_mfam\MFAM24'
    with open(filename,'rb') as f:
        n = 4
        spcr = 4
        off = 16
        mlen = 28
        msg = f.read(off+n*mlen+spcr*n)
        
        for i in range(n):
            start = off+(i)*mlen + spcr*i
            end = off+(i+1)*mlen + spcr*i
            m = msg[start:end]
            tf.parse(m)
            if not tf.hasErrored():
                print('%4d:%4d %s %3d %s' % 
                      (start,
                       end,
                       tf.debug(),
                       len(msg[start:end]),
                       str(msg[start:end])))
            else:
                print('%4d:%4d %s' % (start,end,str(msg[start:end])) )
                
def test_m3xg():
    m = mx3g()
    filename = r'C:\Users\reynolds\Documents\1606_navsea\data\no_i2c.dat'
    msg = get_msg(filename)
    print('msg:%s' % msg)
    m.parse(msg)
    print(m.getData())
    
def get_msg(filename):
    with open(filename,'rb') as f:
        idlen = 6
        msg = f.read(idlen)
        pos = 6
        
        while msg != b'$MFAM1' and pos < 10000:
            msg = msg[1::] + f.read(1)
            pos = pos + 1
            
        wrapper = udp_wrapper()
            
        msg = msg + f.read(36-6)
        pos = pos + 36 - 6
        wrapper.parse(msg)
        
        payload = f.read(wrapper.getLength())
        pos = pos + 1
        return payload
                
if __name__ == '__main__':
    test_mfamfile()
    print()
    test_m3xg()