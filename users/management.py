# -*- coding:utf-8 -*-
# Copyright (c) 2016 MagicStack

from django.db.models.signals import post_migrate
from .models import User


def init_admin_account(**kwargs):
    user = User.objects.create(name='admin', role='SU')
    user.set_password("admin")

post_migrate.connect(init_admin_account, sender=User)





