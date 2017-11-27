#!/usr/bin/env python
#-*-coding:utf-8-*-
# author: 刘奎龙
# date: 2017-11-24
# desc: 该脚本可以实现新增（修改）,查询公钥信息,上传公钥至目标主机功能

from log import info_logger,error_logger,console
import logging
#console.setLevel(logging.ERROR)

import MySQLdb
import traceback
import os
import sys
import paramiko

conn = MySQLdb.connect(
	host='127.0.0.1',
	port=3306,
	user='root',
	passwd='secneo',
	db='pubkey_sys_db',
	charset="utf8"
)

cur = conn.cursor()

#client.connect(host,port,username=user,password=passwd,key_filename=keyname, timeout=4)

def sshcmd(hostname,cmd,port=22,username='secneo',password='********',key_filename='/home/lkl/.ssh/id_rsa'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pkey=key_filename
    key=paramiko.RSAKey.from_private_key_file(pkey)
    #client.connect(hostname,port,username,password,key_filename=private_key, timeout=4)
    client.connect(hostname=hostname, port=port, username=username, password=password, pkey=key, timeout=4)
    stdin, stdout, stderr = client.exec_command(cmd)
    return stderr
    client.close()
        

def query_pubkey(name):
    
    sql = "select * from t_pubkey where name = '%s'" %(name)
    #cur.execute("select * from t_pubkey where name = '%s'"%(name))
    cur.execute(sql)
    try:
       # 执行SQL语句
        cur.execute(sql)
       # 获取所有记录列表
        results = cur.fetchall()
        if len(results):
            res = results[0]
#            for res in results:
#                print u"姓名: %s "%(list(res)[1])
#                print "公钥如下:"
#                print '#'+res[2]
#                print res[3]
            pubkey = "#%s\n%s" %(res[2],res[3])
        else:
            print "无此用户记录"
    except:
#        traceback.print_exc()
        print "无此用户记录"
    finally: 
        conn.close()
    return pubkey
    #return("#%s\n%s" %(res[2],res[3]))
    #return  str('#'+res[2]+'\n'+res[3])

def add_or_update_pubkey(name,tag_name,pubkey):
    sql = "select * from t_pubkey where name = '%s'" %(name)
    cur.execute(sql)
    try:
        cur.execute(sql)
        results = cur.fetchall()
        if len(results):
        #update sql
            update_pubkey_sql = "update t_pubkey set name='%s',tag_name='%s',pubkey='%s' where name='%s'" %(name,tag_name,pubkey,name)
            #info_logger.warning('执行更新sql:%s' %update_pubkey_sql)
            info_logger.warning('执行更新sql')
            try:
                cur.execute(update_pubkey_sql)
                conn.commit()
            except:
                conn.rollback()
        else:
        #insert sql
            insert_pubkey_sql = "insert into t_pubkey(name,tag_name,pubkey) values('%s','%s','%s')" %(name,tag_name,pubkey)
            #info_logger.info('执行插入sql:%s' %insert_pubkey_sql)
            info_logger.info('执行插入sql')
            try:
                cur.execute(insert_pubkey_sql)
                # 提交到数据库执行
                conn.commit()
            except:
                # 发生错误时回滚
                conn.rollback()
    except:
        traceback.print_exc()
    finally: 
        conn.close()


if __name__ == "__main__":
    print "=====================公钥系统==================="
    choice = raw_input(
'''1. 新增(修改)公钥信息
2. 查询公钥信息
3. 主机增加用户公钥
请输入您的选择>> ''')
    try:
        c = int(choice)
        if c == 1:
            name = raw_input('请输入要添加的姓名>> ')
            tag_name = raw_input('请输入要添加的标识名>> ')
            pubkey = raw_input('请输入要添加的公钥内容>> ')
            add_or_update_pubkey(name,tag_name,pubkey)
        elif c == 2:
            name = raw_input('请输入要查询的姓名>> ')
            pubkey = query_pubkey(name)
            print "姓名: %s" %name 
            print "公钥如下:"
            print pubkey
        elif c == 3:
            name = raw_input('请输入用户姓名>> ')
            host = raw_input('请输入目标主机ip>> ')
            port = raw_input('请输入目标主机端口 [22] >> ')
            username = raw_input('请输入目标主机用户名 [secneo] >> ')
            password = raw_input('请输入目标主机密码 [**********] >> ')
            pubkey = query_pubkey(name)
            if not name or not host:
                error_logger.error("参数不足")
                sys.exit()
            if not username or not password or not port:
                username = 'secneo'
                password = 'vm@u7i8o9p0'
                port = 22
                #cmd = "mkdir /home/%s/.ssh && chmod 700 /home/%s/.ssh && echo '%s' >> /home/%s/.ssh/authorized_keys && chmod 600 /home/%s/.ssh/authorized_keys" %(username,username,pubkey,username,username)
                cmd1 = "mkdir /home/%s/.ssh && chmod 700 /home/%s/.ssh" %(username,username)
                cmd2 = "echo '%s' >> /home/%s/.ssh/authorized_keys && chmod 600 /home/%s/.ssh/authorized_keys" %(pubkey,username,username)
                info_logger.info('添加%s的公钥至主机%s' %(name,host))
                sshcmd(hostname=host,cmd=cmd1,username=username,port=port,password=password)
                stderr=sshcmd(hostname=host,cmd=cmd2,username=username,port=port,password=password)
                errlist = stderr.readlines()
                if len(errlist):
                    error_logger.error(errlist)
                else:
                   info_logger.info('添加成功')
            else:
                print "输入有误"
                

    except:
        traceback.print_exc()
