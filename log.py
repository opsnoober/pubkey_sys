#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging

format = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s  [line:%(lineno)d] %(message)s')

#创建日志记录器
info_logger = logging.getLogger('info')

#设置日志级别,小于INFO的日志忽略
info_logger.setLevel(logging.INFO)

#日志记录到磁盘
info_file = logging.FileHandler("info.log")

#设置日志格式
info_file.setFormatter(format)
info_logger.addHandler(info_file)

error_logger = logging.getLogger('error.log')
error_logger.setLevel(logging.ERROR)
error_file = logging.FileHandler("error.log")
error_file.setFormatter(format)
error_logger.addHandler(error_file)

#输出到控制台
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(format)
info_logger.addHandler(console)
error_logger.addHandler(console)

if __name__ == "__main__":
    #写日志
    info_logger.warning("warning message")
    error_logger.error("error message")
    info_logger.info("info message")
