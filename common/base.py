# -*- coding:utf-8 -*-
# Copyright (c) 2016 MagicStack
import uuid
from django.db import models


def gen_uuid():
    return str(uuid.uuid4())


class BaseModel(models.Model):
    id = models.CharField(max_length=128, default=gen_uuid, primary_key=True, help_text=u'唯一标示符')
    create_time = models.DateTimeField(auto_created=True, help_text=u"创建时间")
    modify_time = models.DateTimeField(auto_now=True, help_text=u"修改时间")
    delete_time = models.DateTimeField(auto_now=True, help_text=u"删除时间")
    is_delete = models.BooleanField(default=False)


