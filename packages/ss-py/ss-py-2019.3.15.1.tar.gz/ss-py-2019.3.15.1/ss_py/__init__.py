from aigpy import cmdHelper
from ss_py.sstool import SSTool

def main(argv=None):
    tool = SSTool()
    while True:
        status = '未启动'
        if tool.isSSOpen():
            status = '已启动'
        print(' ======================')
        print(' 0.  退出')
        print(' 1.  启动SS')
        print(' 2.  停止SS')
        print(' -------------')
        print(' 3.  添加用户 ')
        print(' 4.  删除用户')
        print(' 5.  显示用户')
        print('')
        print(' 当前状态: ' + status)
        print('')
        choice = int(cmdHelper.myinput('请输入数字:'))
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
