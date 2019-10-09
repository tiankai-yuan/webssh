import os

from test_webssh import settings


def clean_useless_file():
    # print("清空关于web_ssh的没有用的文件")
    path = settings.MEDIA_ROOT
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
