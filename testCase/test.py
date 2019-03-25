#!usr/bin/python
#encoding:utf-8

from websocket import create_connection

import time
import json

#URL = 'ws://11.11.11.239:9000'
URL = 'ws://127.0.0.1:8080/dis/'
SESSIONID = 0
def buildLoginRequest(uid,pwd):
    """
        @breif 创建登陆dis命令
        @para uid pwd
        @return login命令的json 字符串
    """
    dic = {}
    sender = {"uid":uid, "type":1, "info":" django agent."}
    dic["command"] = "login"
    dic["timestamp"] = int(time.time())
    dic["sender"] = sender
    dic["login"] = {"uid":uid,"pwd":pwd}
    return json.dumps(dic)

def buildCommand(uid,sessionID):
    dic = {}
    sender = {"uid":uid, "type":1, "info":" django agent."}
    dic["command"] = "getLineNetInfo"
    dic["timestamp"] = int(time.time())
    dic["sender"] = sender
    dic["getLineNetInfo"] = {"type":0,"ids":[],'level':0,'direction':0}
    dic['sessionID']= sessionID
    return json.dumps(dic)

def consume():
    ws =  create_connection(URL)
    msg = buildLoginRequest(20037,'1')
    while msg:
        msg = yield ws.send(msg)
        start = time.time()
        ret = ws.recv()
        ret = json.loads(ret)
        global SESSIONID
        print ret
        SESSIONID = ret.get('sessionID',0)
        end = time.time()
        print end-start

def producer(cor):
    cor.send(None)
    count = 0
    start = time.time()
    while count< 2:
        count+=1
        time.sleep(0)
        global SESSIONID
        msg = buildCommand(20037,SESSIONID)
        cor.send(msg)
    try:
        cor.send(0)
    except:
        pass
    end = time.time()
    print "total time is:"
    print end-start
if __name__=="__main__":
    producer(consume())