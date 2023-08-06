from aigpy import cmdHelper
from ss_py.sstool import SSTool

def main(argv=None):
    tool = SSTool()
    while True:
        print('======================')
        print('0  退出')
        print('1  开始')
        print('2  停止')
        print('3  添加')
        print('4  删除')
        print('5  罗列')
        
        choice = int(cmdHelper.myinput('选择:'))
        if choice == 1:
            tool.startSS()
        elif choice == 2:
            tool.stopSS()
        elif choice == 3:
            port = cmdHelper.myinput('端口:')
            pwd = cmdHelper.myinput('密码:')
            tool.addDelPort(True, port, pwd)
        elif choice == 4:
            port = cmdHelper.myinput('端口:')
            tool.addDelPort(False, port, None)
        elif choice == 5:
            ports = tool.getPorts()
            for key,value in ports.items():
                print('{key}:{value}'.format(key = key, value = value))

__all__ = ['main']
