#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HuYuan
# @File    : tools.py
import hashlib
import random
import time


def get_key_obj(pkeyobj, pkey_file=None, pkey_obj=None, password=None):
    if pkey_file:
        with open(pkey_file) as fo:
            try:
                pkey = pkeyobj.from_private_key(fo, password=password)
                return pkey
            except:
                pass
    else:
        try:
            pkey = pkeyobj.from_private_key(pkey_obj, password=password)
            return pkey
        except:
            pkey_obj.seek(0)


def unique():
    ctime = str(time.time())
    salt = str(random.random())
    m = hashlib.md5(bytes(salt, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def parse_time(time_stamp):
    if time_stamp:
        time_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time_stamp)))
        return time_date


def crate_file_name(value1, value2, value3):
    value1 = str(value1)
    value2 = str(value2)
    value3 = str(value3)
    if value2 and value3:
        res = value1 + value2 + value3
    else:
        res = value1
    m = hashlib.md5()  # 括号内也可以传值，类型也要求是bytes类型
    m.update(res.encode('utf-8'))
    return m.hexdigest() + ".json"


def write_to_tmp_file(file_path, datas):
    play_index = 0
    asciinema_head = '{"version": 2, "width": 1500, "height": 1000, "timestamp": 1559530296, "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"}}\n'
    with open(file_path, 'wb') as f:
        f.write(bytes(asciinema_head, encoding='utf-8'))  # 这里是asciinema需要的文件头
        for data in datas:
            play_index += 0.4  # 设置播放速度
            cmd_content = data['cmd_content']
            linestr = '[{}, "o", "{}"]\n'.format(play_index, cmd_content)  # 把命令写入到asciiname文件里面（必须按照这种格式）
            f.write(bytes(linestr, encoding='utf-8'))
