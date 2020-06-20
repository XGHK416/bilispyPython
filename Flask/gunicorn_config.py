import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = "172.24.27.156:5000"
workers = 1
loglevel = 'DEBUG'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = "/www/wwwhome/spider_flask/log/unicorn_access.log"      #访问日志文件
errorlog = "/www/wwwhome/spider_flask/log/gunicorn_error.log"        #错误日志文件
