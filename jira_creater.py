from jira import JIRA
import re
import os
import xdrlib
import sys
import xlrd
import datetime
import time
import commands
reload(sys)
sys.setdefaultencoding( "utf-8" )
# 创建需求
def createfeature():
    print "start to create feature in jira"
    fname = "feature.xlsx"
    bk = xlrd.open_workbook(fname)
    #获取用户名密码
    try:
        login = bk.sheet_by_name("login")
    except:
        print "no sheet in %s named login , can't login jira without it" % fname

    rowl = login.row_values(1)
    jira = JIRA('http://jira.******.com',basic_auth=(rowl[0],rowl[1]))

    #获取需求信息
    try:
        sh = bk.sheet_by_name("info")
    except:
        print "no sheet in %s named info" % fname
    #获取行数
    nrows = sh.nrows
    #获取列数
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows,ncols)

    for i in range(1,nrows):
        rowd = sh.row_values(i)
        if rowd[8] == u'\u65e0':
            issue_dict= {
                'project':{"id":"12400"},
                'issuetype':{'name':"软件需求"},
                'summary':str(rowd[0]),
                'description':str(rowd[1]),
                'customfield_17302':{'value':rowd[2]},      
                'components':[{'name':rowd[3]}],            
                'customfield_16107':[{'value':rowd[4]}],    
                'customfield_16115':{'name':rowd[5]},     
            }
        else:
            issue_dict= {
                'project':{"id":"12400"},
                'issuetype':{'name':"软件需求"},
                'summary':str(rowd[0]),
                'description':str(rowd[1]),
                'customfield_17302':{'value':rowd[2]},      #领域
                'components':[{'name':rowd[3]}],            #模块
                'customfield_16107':[{'value':rowd[4]}],    #产品
                'customfield_16115':{'name':rowd[5]},       #软件经理
                'customfield_16617':{'value':rowd[6]},
            }
        try:
            new_issue = jira.create_issue(fields=issue_dict)
            print new_issue
        except BaseException,e:
            print "create error in %d" %(i + 1)
            e = str(e).split(":")[-1].strip()
            cmd = "cat %s |tail -1" %(e)
            faillog = commands.getoutput(cmd)
            print faillog
# 创建缺陷
def createbug():
    print "start to create bug in jira"
    fname = "bug.xlsx"
    bk = xlrd.open_workbook(fname)

    #获取用户名密码
    try:
        login = bk.sheet_by_name("login")
    except:
        print "no sheet in %s named login , can't login jira without it" % fname

    rowl = login.row_values(1)
    jira = JIRA('http://jira.zeusis.com',basic_auth=(rowl[0],rowl[1]))

    #get bug info and create
    try:
        sh = bk.sheet_by_name("info")
    except:
        print "no sheet in %s named info" % fname
    #获取行数
    nrows = sh.nrows
    #获取列数
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows,ncols)

    for i in range(1,nrows):
        rowd = sh.row_values(i)
        issue_dict= {
            'project':{"key":rowd[0]},
            'issuetype':{'name':"缺陷"},
            'summary':str(rowd[1]),
            'description':str(rowd[2]),
            'customfield_17302':{'value':rowd[3]},      #领域
            'components':[{'name':rowd[4]}],            #模块
            'assignee':{'name':rowd[5]},
            'versions':[{'name':rowd[6]}],
            'customfield_15121':{'value':rowd[7]},
        }
        try:
            new_issue = jira.create_issue(fields=issue_dict)
            print new_issue
        except BaseException,e:
            print "create error in %d" %(i + 1)
            e = str(e).split(":")[-1].strip()
            cmd = "cat %s |tail -1" %(e)
            faillog = commands.getoutput(cmd)
            print faillog

def createcomponent():
    print "start to create component in jira"
    fname = "demo3.xls"
    bk = xlrd.open_workbook(fname)

    #获取用户名密码
    try:
        login = bk.sheet_by_name("login")
    except:
        print "no sheet in %s named login , can't login jira without it" % fname

    rowl = login.row_values(1)
    jira = JIRA('http://172.16.3.139:80/',basic_auth=('admin','admin'))
    project = 'PSR'
    #获取模块信息
    try:
        sh = bk.sheet_by_name("info")
    except:
        print "no sheet in %s named info" % fname

    nrows = sh.nrows
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows,ncols)

    #创建模块
    for i in range(1,nrows):
        rowd = sh.row_values(i)
        try:
            new_component = jira.create_component(rowd[0],project,description=rowd[1],leadUserName=rowd[2],assigneeType='COMPONENT_LEAD',isAssigneeTypeValid=True)
            print new_component
        except BaseException,e:
            print "create error in %d" %(i + 1)
            e = str(e).split(":")[-1].strip()
            cmd = "cat %s |tail -1" %(e)
            faillog = commands.getoutput(cmd)
            print faillog

def createfeaturetest():
    print "start to create feature in jira"
    fname = "feature.xlsx"
    bk = xlrd.open_workbook(fname)

    # 获取用户名密码
    try:
        login = bk.sheet_by_name("login")
    except:
        print "no sheet in %s named login , can't login jira without it" % fname

    rowl = login.row_values(1)
    jira = JIRA('http://10.3.11.103:80/', basic_auth=(rowl[0], rowl[1]))
    project=rowl[2]
    print project
    # 获取需求信息
    try:
        sh = bk.sheet_by_name("info")
    except:
        print "no sheet in %s named info" % fname
    # 获取行数
    nrows = sh.nrows
    # 获取列数
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows, ncols)

    for i in range(1, nrows):
        rowd = sh.row_values(i)
        print rowd[0],rowd[1],rowd[2],rowd[3],rowd[4],rowd[5],rowd[6],rowd[7],rowd[8],rowd[9]
        issue_dict = {
            'project': {"key": project},
            'issuetype': {'name': "软件需求"},
            'summary': str(rowd[0]),
            'description': str(rowd[1]),
            'customfield_19101': {'value': rowd[2], 'child': {'value': rowd[3]}},  # 领域和模块
            # 'customfield_17302': {'value': rowd[2]},  # 领域
            # 'components': [{'name': rowd[3]}],  # 模块
            'customfield_19105': {'value': rowd[4]},  # 功能点
            'customfield_19102': {'value': rowd[5]},  # 需求状态
            'customfield_19103': {'value': rowd[6],'child':{'value':rowd[7]}},  #需求来源2
            'customfield_19104': str(rowd[8]),  # 需求编号
            # 'assignee': {'name': rowd[9]},#处理人
        }

        try:
            new_issue = jira.create_issue(fields=issue_dict)
            print new_issue
        except BaseException, e:
            print "create error in %d" % (i + 1)
            e = str(e).split(":")[-1].strip()
            cmd = "cat %s |tail -1" % (e)
            faillog = commands.getoutput(cmd)
            print faillog


def createfeaturezhengshi():
    print "start to create feature in jira"
    fname = "feature.xlsx"
    bk = xlrd.open_workbook(fname)

    # 获取用户名密码
    try:
        login = bk.sheet_by_name("login")
    except:
        print "no sheet in %s named login , can't login jira without it" % fname

    rowl = login.row_values(1)
    print type(rowl[0])
    print type(rowl[1])
    if isinstance(rowl[0],float) and rowl[0]==int(rowl[0]):
        rowl[0]=int(rowl[0])
    if isinstance(rowl[1],float) and rowl[1] == int(rowl[1]):
        rowl[1] = int(rowl[1])
    print rowl[0],rowl[1]
    jira = JIRA('http://172.16.3.139:80/', basic_auth=((rowl[0]), rowl[1]))
    project=rowl[2]
    print project
    # 获取需求信息
    try:
        sh = bk.sheet_by_name("info")
    except:
        print "no sheet in %s named info" % fname
    # 获取行数
    nrows = sh.nrows
    # 获取列数
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows, ncols)

    for i in range(1, nrows):
        rowd = sh.row_values(i)
        print rowd[0],rowd[1],rowd[2],rowd[3],rowd[4],rowd[5],rowd[6],rowd[7],rowd[8]
        if project=='PSR':
            issue_dict = {
                'project': {"key": project},
                'issuetype': {'name': "软件需求"},
                'customfield_19105': {'value': rowd[0]},  # 需求的来源
                'customfield_19106': {'value': rowd[1]},  # 需求版本号
                'customfield_19102': str(rowd[2]),  # 运营商需求编号
                'customfield_17302': {'value': rowd[3]},  # 领域
                'components': [{'name': rowd[4]}],  # 模块
                'customfield_19100': str(rowd[5]),  # 一级需求
                'summary': str(rowd[6]),
                'description': str(rowd[7]),
                # 'customfield_19101': {'value': rowd[2], 'child': {'value': rowd[3]}},  # 领域和模块
                'customfield_19104': {'value': rowd[8]},  # 需求是否有效

                # 'customfield_19101': {'value': rowd[6],'child':{'value':rowd[7]}},  #需求的来源

                # 'assignee': {'name': rowd[9]},#处理人
            }
        else:
            issue_dict = {
                'project': {"key": project},
                'issuetype': {'name': "软件需求"},
                'customfield_19105': {'value': rowd[0]},  # 需求的来源
                'customfield_19106': {'value': rowd[1]},  # 需求版本号
                'customfield_19102': str(rowd[2]),  # 运营商需求编号
                'customfield_17302': {'value': rowd[3]},  # 领域
                'components': [{'name': rowd[4]}],  # 模块
                'customfield_19100': str(rowd[5]),  # 一级需求
                'summary': str(rowd[6]),
                'description': str(rowd[7]),
                # 'customfield_19101': {'value': rowd[2], 'child': {'value': rowd[3]}},  # 领域和模块
                # 'customfield_19104': {'value': rowd[8]},  # 需求是否有效

                # 'customfield_19101': {'value': rowd[6], 'child': {'value': rowd[7]}},  # 需求的来源

                # 'assignee': {'name': rowd[9]},#处理人
            }

        try:
            new_issue = jira.create_issue(fields=issue_dict)
            print new_issue
        except BaseException, e:
            print e
            print "create error in %d" % (i + 1)
            e = str(e).split(":")[-1].strip()
            cmd = "cat %s |tail -1" % (e)
            faillog = commands.getoutput(cmd)
            print faillog


if __name__ == "__main__":
    # createcomponent()
    # createfeaturetest()
    createfeaturezhengshi()
    print "ok"

