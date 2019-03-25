import json
import time
from enum import Enum

class ErrorCodes(Enum):
    errorNone = 0 #没有错误
    illegalMessage = 1 #webscoket 接受的消息不能被json解析
    illegalConnection = 2  #没有登陆
    illegalUid = 3
    illegalCommand = 4  #command 没有对应的处理器
    excuteSqlFailed = 5 #执行sql语句错误
class Message:
    """
       a message Tool class
    """
    @classmethod
    def errorMsg(cls,error):
        error = {"code":error.value,"description":error.name}
        return error
    
    @classmethod
    def okayMsg(cls):
        pass
    @classmethod
    def buildMsgNoRequestAndSender(cls,command,body):
        response = {}
        response["command"] = command
        response[command] = body
        response["timestamp"] = time.time()
        return response

    @classmethod
    def buildResponse(cls,request,sender,command,body,sessionID = None,flag=None):

        response = {}
        response["request"] = request
        response["sender"] = sender
        response["command"] = command
        if not sessionID == None:
            response["sessionID"] = sessionID
        if not flag == None:
            response["flag"] = flag
        response["timestamp"] = time.time()
        response["MD5"] = ''
        response[command] = body

        return response

    @classmethod
    def buildRequestToResponse(cls,uid,command,timestamp):
        request = {}
        request["uid"] = uid
        request["command"] = command
        request["timestamp"] = timestamp
        return request
    
    @classmethod
    def buildResponseFromMsg(cls,msg,command,body,sessionID=None,flag=None):
        response = {}
        response["request"] = cls.parseRequestFromMsg(msg)
        response["sender"] = cls.parseSenderFromMsg(msg)
        response["command"] = command
        response[command] = body
        response["MD5"]=""
        response["timestamp"] = time.time()
        if sessionID:
            response["sessionID"] = sessionID
        if flag :
            response["flag"] = flag

        return response

    @classmethod
    def parseRequestFromMsg(cls,msg):
        request = { "uid":msg["sender"]["uid"],"command":msg["command"],"timestamp":msg["timestamp"]}
        return request
    @classmethod
    def parseSenderFromMsg(cls,msg):
        return msg["sender"]
    
    @classmethod
    def buildSenderToResponse(cls,address,uid,msgtype,info):
        sender =  {"address":address,"uid":uid,"type":msgtype,"info":info}
        return sender

    @classmethod
    def checkMessage(cls,msg):
        """
            如果msg不能被json转换，返回空字符
            如果msg能被json转换，返回dict
            待优化：检查msg的字段值
        """
        data = ''
        try:
            data = json.loads(msg)
        except:
            data = ''
        return data