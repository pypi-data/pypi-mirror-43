import sys
import subprocess

from ss_py.ssprofile import SSProfile

# PATH_BASE = './'
PATH_BASE = '/etc/ss_py/'
FILE_PROFILE = PATH_BASE + 'profile.json'
FILE_SSERVER_PID = PATH_BASE + 'sserverpid.txt'

class SSTool(object):
    def __init__(self):
        self.profile = SSProfile(FILE_PROFILE)

    def _checkPortRanges(self, port):
        port = int(port)
        if port > 0 and port <= 65536:
            return True
        return False

    def startSS(self):
        cmd = 'ssserver -qq -c ' + FILE_PROFILE + ' 2>/dev/null >/dev/null & echo $! > ' + FILE_SSERVER_PID
        res = subprocess.call(cmd, shell=True)
        return res

    def stopSS(self):
        cmd = 'kill `cat ' + FILE_SSERVER_PID + '`'
        res = subprocess.call(cmd, shell=True)
        return
    
    def addDelPort(self, isAdd, port, pwd):
        if self._checkPortRanges(port) == False:
            return False
        if isAdd:
            self.profile.addPort(port, pwd)
        else:
            self.profile.delPort(port)
        self.profile.save(FILE_PROFILE)
        self.stopSS()
        self.startSS()
    
    


