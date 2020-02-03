# -*- coding: utf-8 -*-
import datetime

from Flask.util.enum import TaskList,Status


def _init():
    global _global_dict
    _global_dict = {
        'total_user': 0,
        'total_video': 0,
        'current_user': 0,
        'current_video': 0,
        'current_task': TaskList.no_task.value,
        'start_time': datetime.datetime.now(),
        'have_time': datetime.datetime.now(),
        'status': Status.Wait.value
    }


def return_dict():
    return _global_dict


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


def set_zero(name):
    _global_dict[name] = 0
