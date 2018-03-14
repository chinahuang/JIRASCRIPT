# -*- coding: utf-8 -*-

import jira
import ConfigParser
import MySQLdb
import logging
import sys
import json

config = ConfigParser.ConfigParser()
config.read("jira_feature.conf")

mysql_host=config.get("mysql","host")
mysql_user=config.get("mysql","user")
mysql_password=config.get("mysql","password")
mysql_database=config.get("mysql","database")
jira_url=config.get("jira","url")
jira_user=config.get("jira","user")
jira_password=config.get("jira","password")

def create_table(project_name,is_main=False):
    checkForeign(False)
    cursor.execute("drop table if EXISTS " + project_name)
    if  is_main:
        sql="""create table """+project_name+""" (
        issue_key char(30) NOT NULL primary key,
        issue_source char(50) NOT NULL,
        issue_version char(50) NOT NULL,
        issue_number  char(50) NOT NULL,
        issue_first  char(200) NOT NULL,
        issue_second char(255) NOT NULL,
        issue_relate boolean default false)"""
    else:
        sql = """create table """ + project_name + """ (
                issue_key char(30) NOT NULL primary key,
                psr_key char(30), 
                issue_source char(50) NOT NULL,
                issue_version char(50) NOT NULL,
                issue_number  char(50) NOT NULL,
                issue_first  char(200) NOT NULL,
                issue_second char(255) NOT NULL,
                issue_relate boolean default false,
                FOREIGN KEY (psr_key) REFERENCES PSR (issue_key))"""
    try:
        cursor.execute(sql)
        print "create table ok"
        checkForeign(True)
    except Exception ,e:
        print "create table fail"
        print e

def checkForeign(check=False):
    if check:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    else:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")


def insert_proj(project_name,is_main=False):
    field_list=['customfield_19105','customfield_19100','customfield_19106','customfield_19102','customfield_17302','components','summary']
    issues=jira_work.search_issues('project = '+project_name+' AND issuetype = 软件需求',maxResults=100000,
                                   fields=field_list)
    checkForeign(False)
    with open(project_name+".txt","w+") as project_need_file:
        for i in issues:
            if i.fields.customfield_19102 is None or i.fields.customfield_19105 is None or i.fields.customfield_19106 is None :
                print i.key+" is bad"
            else :
                print i.key+" is ok"
                need_info={}
                need_info['key']=i.key
                need_info['num']=i.fields.customfield_19102
                need_info['source']=i.fields.customfield_19105.value
                need_info['version']=i.fields.customfield_19106.value
                need_info['first']=i.fields.customfield_19100
                need_info['second']=i.fields.summary
                project_need_file.write(str(need_info)+"\n")
                # soft_need= i.raw['fields']['customfield_19105']
                # if soft_need is not None:
                #     print soft_need
                # print i.raw
                try :
                    param=(need_info['key'],need_info['source'],need_info['version'],need_info['num'],need_info['first'],
                           need_info['second'],0)
                    sql="insert into "+project_name+"(issue_key,issue_source" \
                                                    ",issue_version,issue_number," \
                                                    "issue_first,issue_second,issue_relate) " \
                                                    "values ('%s','%s','%s','%s','%s','%s',%d)" %(need_info['key'],need_info['source'],need_info['version'],need_info['num'],need_info['first'],
                           need_info['second'],0)
                    print sql
                    cursor.execute(sql)
                    db.commit()
                except Exception ,e:
                    print e
                    db.rollback()
    checkForeign(True)




def project_num():
    projects=jira_work.projects()
    for i in projects:
        print i.key

def get_psr(project_name):
    try:
        sql="select issue_key,issue_source,issue_version,issue_number,issue_first,issue_second,issue_relate from "+project_name
        print sql
        cursor.execute(sql)
        results=cursor.fetchall()
        print "the length of "+project_name+" is "+ str(len(results))
        pro_str={}
        for i in results:
            # if i[6] == 0:
            str_one=""
            str_one=i[1]+i[2]+i[3]+i[4]+i[5]
            pro_str[i[0]]=str_one
        print  project_name+" not link number is "+str(len(pro_str))
        sql = "select issue_key,issue_source,issue_version,issue_number,issue_first,issue_second,issue_relate from PSR"
        print sql
        cursor.execute(sql)
        results = cursor.fetchall()
        print "the length of PSR  is " + str(len(results))
        psr_str = {}
        for i in results:
            str_one=""
            str_one = i[1] + i[2] + i[3] + i[4] + i[5]
            psr_str[i[0]] = str_one
        print "PSR not link number is "+str(len(psr_str))
        link_pro=0
        with open(project_name+"_link.txt",'w') as pro_link:
            for i in pro_str:
                for j in psr_str:
                    if pro_str[i]==psr_str[j]:
                        pro_link.write(i+" : "+pro_str[i]+"   ------>   "+j+" : "+psr_str[j]+" \n")
                        try:
                            sql="update "+project_name+" set psr_key='%s',issue_relate=1 where issue_key='%s'"%(j,i)
                            print sql
                            cursor.execute(sql)
                            sql="update psr set issue_relate=1 where issue_key='%s'"%j
                            db.commit()
                            print sql
                            cursor.execute(sql)
                            db.commit()
                        except Exception ,e:
                            db.rollback()
                            print e
                        try:
                            jira_work.create_issue_link(type="Relates", inwardIssue=i, outwardIssue=j,)
                        except Exception as e:
                            print e
                        link_pro+=1
            print project_name+" link to psr is "+str(link_pro)


    except Exception ,e:
        print e

def create_link(link_type,psr_num,pro_num):
    if link_type == 'relate':
        name = 'Relates'
        inward = 'relates to'
        outward = 'relates to'
        restful_link=jira_work.issue(pro_num).self
        link_tmp['update']['issuelinks'][0]['add']['type']['name'] = name
        link_tmp['update']['issuelinks'][0]['add']['type']['inward'] = inward
        link_tmp['update']['issuelinks'][0]['add']['type']['outward'] = outward
        link_tmp['update']['issuelinks'][0]['add']['outwardIssue'] = psr_num
        link_json = json.dumps(link_tmp)
        link_order="curl -D- -u  %s:%s --connect-timeout 30 --max-time 30 -X PUT --data %s -H 'Content-Type: application/json' %s"%(jira_user,jira_password,link_json,restful_link)
        jira_work.create_issue_link(type="Relates",inwardIssue=pro_num,outwardIssue=psr_num,)
        print link_order




try:
    db= MySQLdb.connect(mysql_host,mysql_user,mysql_password,mysql_database)
    jira_work = jira.JIRA(jira_url, basic_auth=(jira_user,jira_password))
    tmp=open('tmp.txt','r')
    link_tmp = eval(tmp.read())
    print "success to connect the database"
    cursor = db.cursor()
    # create_table("PSR",is_main=True)
    # create_table("GOLIATH",is_main=False)

    # insert_proj("GOLIATH")
    get_psr("GOLIATH")
    # create_link('relate','PSR-6300','GOLIATH-2368')

except Exception as e :
    print "fail to connect the database "
    print e.message
finally:
    db.close()
    tmp.close()
    print "success to close the database"


















