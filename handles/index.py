from base.handle import BaseHttp,BaseWebscoket

import logging
from tornado import gen
from base.messages import Message,ErrorCodes

from handles.dataHandle import loginHandle

class IndexHandle(BaseHttp):
    
    def initialize(self):
        self.db_pool = self.application.db_pool
        self.sessions = self.application.Sessions
        self.dispatcher = self.application.dispatcher

    def get(self):
        import json
        return self.write(json.dumps(self.sessions.listAll()))

class WsHandle(BaseWebscoket):

    def initialize(self):
        self.db_pool = self.application.db_pool
        self.sessions = self.application.Sessions
        self.dispatcher = self.application.dispatcher

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        self.set_nodelay(True)
        
    def on_close(self):
        #WsHandle.waiters.remove(self)
        #删除socket缓存信息
        self.sessions.removeSessionBySocket(self)

    @gen.coroutine
    def replyText(self,msg):
        ret = False
        try:
           ret = yield self.write_message(msg)
        except:
            return ret
        return ret
    @gen.coroutine
    def on_message(self, message):
        #check message
        msg = Message.checkMessage(message)

        #接受到的消息不能被json解析
        if not msg:
            error = ErrorCodes.illegalMessage
            body = Message.errorMsg(error)
            response = Message.buildMsgNoRequestAndSender('error',body)
            yield self.replyText(response)
            return
        uid = msg['sender']['uid']
        command = msg['command']

        #如果用户没有session,给用户创建一个session
        if not self.sessions.findSessionByUid(uid):
            self.sessions.createNewSession(uid,self)
        #如果session已经存在，update session
        else:
            self.sessions.updateSessionByUid(uid,self)
        #checkLogin
        #用户没有登陆，
        if not self.sessions.checkLogin(uid):
            # command 不是login，回复非法连接
            if not command =='login':
                error = ErrorCodes.illegalConnection
                body = Message.errorMsg(error)
                response = Message.buildResponseFromMsg(msg,'error',body)
                yield self.replyText(response)
                return 
            else:
                #登陆处理
                ret = yield loginHandle(self.sessions,self.db_pool,msg)
                if not ret:
                    error = ErrorCodes.illegalCommand
                    body = Message.errorMsg(error)
                    response = Message.buildResponseFromMsg(msg,'error',body)
                    yield self.replyText(response)
                    return 
        #用户已经登陆过了
        else:
            #分发command 处理
            ret = yield self.dispatcher.dispatch(self.sessions,self.db_pool,msg)
            print(msg)
            if not ret:
                error = ErrorCodes.illegalCommand
                body = Message.errorMsg(error)
                response = Message.buildResponseFromMsg(msg,'error',body)
                yield self.replyText(response)
       


        
        
        
       