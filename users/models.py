# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
import time

from common.base import gen_uuid


class UserGroup(models.Model):
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('SU', 'SuperUser'),
        ('GA', 'GroupAdmin'),
        ('CU', 'CommonUser'),
    )
    id = models.CharField(max_length=128, default=gen_uuid, primary_key=True, help_text=u'唯一标示符')
    role = models.CharField(max_length=2, choices=USER_ROLE_CHOICES, default='CU')
    group = models.ManyToManyField(UserGroup)
    create_time = models.DateTimeField(auto_created=True, help_text=u"创建时间")
    modify_time = models.DateTimeField(auto_now=True, help_text=u"修改时间")
    delete_time = models.DateTimeField(auto_now=True, help_text=u"删除时间")
    is_delete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username


class AdminGroup(models.Model):
    """
    under the user control group
    用户可以管理的用户组，或组的管理员是该用户
    """

    user = models.ForeignKey(User)
    group = models.ForeignKey(UserGroup)

    def __unicode__(self):
        return '%s: %s' % (self.user.username, self.group.name)

