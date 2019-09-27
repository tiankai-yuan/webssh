import datetime
import json
import re
from threading import Thread

import paramiko

from app01 import models
from app01.tools.tools import get_key_obj


class SSH:
    def __init__(self, websocker, message):
        self.websocker = websocker
        self.message = message
        self.login_time = datetime.datetime.now()
        self.cmd = ''
        self.res = ''
        self.res1 = ''
        self.t_s = ""
        self.log_obj = None
        self.ctrl_dict = {"ctrlR": False, "ctrl_data": None}

    # term 可以使用 ansi, linux, vt100, xterm, dumb，除了 dumb外其他都有颜色显示
    def connect(self, host, user, password=None, ssh_key=None, port=22, timeout=30,
                term='ansi', pty_width=80, pty_height=24, terminal_id=None):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if ssh_key:
                key = get_key_obj(paramiko.RSAKey, pkey_obj=ssh_key, password=password) or \
                      get_key_obj(paramiko.DSSKey, pkey_obj=ssh_key, password=password) or \
                      get_key_obj(paramiko.ECDSAKey, pkey_obj=ssh_key, password=password) or \
                      get_key_obj(paramiko.Ed25519Key, pkey_obj=ssh_key, password=password)

                ssh_client.connect(username=user, hostname=host, port=port, pkey=key, timeout=timeout)
            else:
                ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)

            # 登录进来进行用户信息保存
            self.login_org_user = "admin"
            self.login_org_name = "CBC"
            self.login_as_user = user
            self.terminal_id = terminal_id

            transport = ssh_client.get_transport()
            self.channel = transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()

            for i in range(2):
                recv = self.channel.recv(1024).decode('utf-8')
                self.message['status'] = 0
                self.message['message'] = recv
                message = json.dumps(self.message)
                self.websocker.send(message)
                self.res += recv

            # 创建3个线程将服务器返回的数据发送到django websocket（1个线程都可以）
            Thread(target=self.websocket_to_django).start()
            # Thread(target=self.websocket_to_django).start()
            # Thread(target=self.websocket_to_django).start()
        except:
            self.message['status'] = 2
            self.message['message'] = 'connection faild...'
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.websocker.close(3001)

    def resize_pty(self, cols, rows):
        self.channel.resize_pty(width=cols, height=rows)

    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
            if data == '\r':
                data = '\n'
            self.cmd += data
        except:
            self.close()

    def save_commend(self, data):  # 这里是保存命令的方法
        obj = models.LogCommandResult()
        obj.node_id = "node_id"
        obj.login_as_user = self.login_as_user
        obj.login_org_user = self.login_org_user
        obj.login_org_name = self.login_org_name
        obj.login_time = self.login_time
        obj.terminal_id = self.terminal_id
        obj.cmd_content = json.dumps(data)[1:-1]
        obj.save()

    def websocket_to_django_bak(self):
        try:
            while True:
                data = self.channel.recv(1024).decode("utf-8")
                # print("BYTE:   ", data.encode())
                # print("STR:   ", data)
                # tudo 监听Ctrl + R
                self.save_commend(data=str(data))
                if "reverse-i-search" in data:
                    # {"ctrlR": None, "ctrl_data": None}
                    self.ctrl_dict["ctrlR"] = True
                if self.ctrl_dict["ctrlR"] and b'\n' in data.encode():
                    self.channel.send("history")
                    self.ctrl_dict["ctrlR"] = False

                if not len(data):
                    return
                self.message['status'] = 0
                self.message['message'] = data
                self.res += data
                message = json.dumps(self.message)
                self.websocker.send(message)

                tmp1 = data.encode()
                if re.findall(b"^(\x07)+", tmp1):
                    continue

                if re.findall(b'^(\x1b\[D\x1b\[D)', tmp1):
                    # tudo处理字符串乱码问题
                    # print(tmp1)
                    # res = re.split(b"\x1b\[D\x1b\[D", tmp1)
                    # a = re.split(b'\x1b\[\d?[K|P]', res[-1])
                    # t = [j for j in a if len(j) > 0 and b'\x1b' not in j]
                    # data = t[0].decode()
                    # print(data)

                    # 处理上下键 self.t_s 用于存放上一个传过来的data
                    self.res1 = self.res1.rstrip(self.t_s)
                    if not self.res1.endswith(" "):
                        self.res1 += " "
                if b'\x1b[D\x1b[K' in tmp1:
                    # 这是删除操作
                    self.res1 = self.res1.encode().rstrip(tmp1)
                    # 删除的退格键，有的时候不是一个个来的。若退格键一次性来两个，则需删两个字符
                    up_time = tmp1.count(b'\x1b[D\x1b[K')
                    self.res1 = self.res1.decode("utf-8")[:-up_time]
                # if tmp1 == b'\x1b[D':
                #     print(data.split("\"")[0])
                #     self.res1 = self.res1[:-1] + data.split("\"")[0] + self.res1[-1]
                # if tmp1 == b'\x1b[C':
                #     self.res1 = self.res1[:-1] + data + self.res1[-1]
                self.res1 += data
                self.t_s = data
        except Exception as e:
            print(e)
            self.close()

    def websocket_to_django(self):
        try:
            while True:
                data = self.channel.recv(1024).decode("utf-8")
                if not len(data):
                    return
                self.message['status'] = 0
                self.message['message'] = data
                self.res += data
                message = json.dumps(self.message)
                self.websocker.send(message)
                self.save_commend(data=str(data))
        except Exception as e:
            print(e)
            self.close()

    def close(self):
        self.message['status'] = 1
        self.message['message'] = 'connection closed...'
        message = json.dumps(self.message)
        self.websocker.send(message)
        self.channel.close()
        self.websocker.close()

    def shell(self, data):
        # 原作者使用创建线程的方式发送数据到ssh，每次发送都是一个字符，可以不用线程
        # 直接调用函数性能更好
        # Thread(target=self.django_to_ssh, args=(data,)).start()
        self.django_to_ssh(data)

        # 原作者将发送数据到django websocket的线程创建函数如果写到这，会导致每在客户端输入一个字符就创建一个线程
        # 最终可能导致线程创建太多，故将其写到 connect 函数中
        # Thread(target=self.websocket_to_django).start()
