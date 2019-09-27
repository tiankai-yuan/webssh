from uuid import uuid4

from django.db import models


# Create your models here.

class LogCommandResult(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid4)
    node_id = models.CharField(max_length=45, null=False)
    terminal_id = models.CharField(max_length=45, null=False)
    login_as_user = models.CharField(max_length=45, null=False)
    login_org_user = models.CharField(max_length=45, null=False)
    login_org_name = models.CharField(max_length=45, null=False)
    cmd_content = models.TextField(null=True)
    login_time = models.DateTimeField(auto_now_add=False, null=False)
    recode_time = models.DateTimeField(auto_now=True, null=False)
    logout_time = models.DateTimeField(null=True)

    @classmethod
    def create_login_obj(cls, data_dic: dict):
        o = cls.objects.create(**data_dic)
        return o

    def msg_update(self, msg, logout_time=None):
        self.cmd_content = msg
        self.logout_time = logout_time
        self.save()

    @classmethod
    def get_cmd_content(cls, terminal_id, start_time=None, end_time=None):
        if start_time and end_time:
            query_values = {
                "start_time": start_time,
                "end_time": end_time,
                "terminal_id": terminal_id
            }
        else:
            query_values = {
                "terminal_id": terminal_id
            }
        cmd_content_list = cls.objects.filter(**query_values).order_by("recode_time").values('cmd_content')
        return cmd_content_list

    class Meta:
        managed = True
        # abstract = False
        app_label = 'app01'
        db_table = 'log_command_result'
        # 如果要将迁移应用到本地测试数据库，managed 改为 True
        # 为防止更改生产环境中的数据库，迁移过后务必改回 False
        # managed 属性不会被子类继承，需要把子类的 Meta 设为 class Meta(LogCommandResult.Meta)
