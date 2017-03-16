# -*- coding:utf-8 -*-
from django.core.mail import send_mail

from common.utils import get_object
from .models import *


def group_add_user(group, user_id=None, username=None):
    """
    用户组中添加用户
    UserGroup Add a user
    """
    if user_id:
        user = get_object(User, id=user_id)
    else:
        user = get_object(User, username=username)

    if user:
        group.user_set.add(user)


def db_add_group(**kwargs):
    """
    add a user group in database
    数据库中添加用户组
    """
    name = kwargs.get('name')
    group = get_object(UserGroup, name=name)
    users = kwargs.pop('users_id')

    if not group:
        group = UserGroup(**kwargs)
        group.save()
        for user_id in users:
            group_add_user(group, user_id)


def group_update_member(group_id, users_id_list):
    """
    user group update member
    用户组更新成员
    """
    group = get_object(UserGroup, id=group_id)
    if group:
        group.user_set.clear()
        for user_id in users_id_list:
            user = get_object(UserGroup, id=user_id)
            if isinstance(user, UserGroup):
                group.user_set.add(user)


def db_add_user(**kwargs):
    """
    add a user in database
    数据库中添加用户
    """
    groups_post = kwargs.pop('groups')
    admin_groups = kwargs.pop('admin_groups')
    role = kwargs.get('role', 'CU')
    user = User(**kwargs)
    user.set_password(kwargs.get('password'))
    user.save()
    if groups_post:
        group_select = []
        for group_id in groups_post:
            group = UserGroup.objects.filter(id=group_id)
            group_select.extend(group)
        user.group = group_select

    if admin_groups and role == 'GA':  # 如果是组管理员就要添加组管理员和组到管理组中
        for group_id in admin_groups:
            group = get_object(UserGroup, id=group_id)
            if group:
                AdminGroup(user=user, group=group).save()
    return user


def db_update_user(**kwargs):
    """
    update a user info in database
    数据库更新用户信息
    """
    groups_post = kwargs.pop('groups')
    admin_groups_post = kwargs.pop('admin_groups')
    user_id = kwargs.pop('user_id')
    user = User.objects.filter(id=user_id)
    if user:
        user_get = user[0]
        password = kwargs.pop('password')
        user.update(**kwargs)
        if password.strip():
            user_get.set_password(password)
            user_get.save()
    else:
        return None

    group_select = []
    if groups_post:
        for group_id in groups_post:
            group = UserGroup.objects.filter(id=group_id)
            group_select.extend(group)
    user_get.group = group_select

    if admin_groups_post != '':
        user_get.admingroup_set.all().delete()
        for group_id in admin_groups_post:
            group = get_object(UserGroup, id=group_id)
            AdminGroup(user=user, group=group).save()


def db_del_user(username):
    """
    delete a user from database
    从数据库中删除用户
    """
    user = get_object(User, username=username)
    if user:
        user.delete()


def user_add_mail(user, kwargs):
    """
    add user send mail
    发送用户添加邮件
    """
    user_role = {'SU': u'超级管理员', 'GA': u'组管理员', 'CU': u'普通用户'}
    mail_title = u'恭喜你的跳板机用户 %s 添加成功 Jumpserver' % user.name
    mail_msg = u"""
    Hi, %s
        您的用户名： %s
        您的权限： %s
        您的web登录密码： %s
        您的ssh密钥文件密码： %s
        密钥下载地址： %s/juser/key/down/?uuid=%s
        说明： 请登陆跳板机后台下载密钥, 然后使用密钥登陆跳板机！
    """ % (user.name, user.username, user_role.get(user.role, u'普通用户'),
           kwargs.get('password'), kwargs.get('ssh_key_pwd'), '', user.uuid)
    send_mail(mail_title, mail_msg, '', [user.email], fail_silently=False)


def get_display_msg(user, password='', ssh_key_pwd='', send_mail_need=False):
    if send_mail_need:
        msg = u'添加用户 %s 成功！ 用户密码已发送到 %s 邮箱！' % (user.name, user.email)
    else:
        msg = u"""
        跳板机地址： %s <br />
        用户名：%s <br />
        密码：%s <br />
        密钥密码：%s <br />
        密钥下载url: %s/juser/key/down/?uuid=%s <br />
        该账号密码可以登陆web和跳板机。
        """ % ('', user.username, password, ssh_key_pwd, '', user.uuid)
    return msg
