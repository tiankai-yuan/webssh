import os

from django.shortcuts import render, HttpResponse
from django.views.generic import View

from app01.tools.tools import parse_time, write_to_tmp_file, crate_file_name
from app01.tools.tools import unique
from test_webssh.settings import TMP_DIR, MEDIA_ROOT
from .models import LogCommandResult
from .myforms import LogCommandForm


def index(request):
    return render(request, 'index.html')


def upload_ssh_key(request):
    if request.method == 'POST':
        pkey = request.FILES.get('pkey')
        ssh_key = pkey.read().decode('utf-8')

        while True:
            filename = unique()
            ssh_key_path = os.path.join(TMP_DIR, filename)
            if not os.path.isfile(ssh_key_path):
                with open(ssh_key_path, 'w') as f:
                    f.write(ssh_key)
                break
            else:
                continue

        return HttpResponse(filename)


class CommandData(View):
    def get(self, request):
        '''
        获取用户选择的参数以返回视频文件
        :param request:
        :return:
        '''

        myform = LogCommandForm(request.GET)
        if myform.is_valid():
            start_time = request.GET.get("start_time")  # 前端过来的是str类型的时间戳
            myform.cleaned_data["start_time"] = parse_time(start_time)

            end_time = request.GET.get("end_time")
            myform.cleaned_data["end_time"] = parse_time(end_time)
            terminal_id = myform.cleaned_data.get("terminal_id")

            file_name = crate_file_name(terminal_id, start_time, end_time)
            file_path = os.path.join(MEDIA_ROOT, file_name)
            if not os.path.exists(file_path):
                datas = LogCommandResult.get_cmd_content(**myform.cleaned_data)
                write_to_tmp_file(file_path, datas)
            return render(request, 'playback_commend.html', locals())
        return HttpResponse("缺少参数")
