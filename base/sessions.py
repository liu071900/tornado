import time
from tornado import gen

class Session(object):
    """"
        邦定webscoket对象和用户信息的对象
    """
    def __init__(self,id,uid,ws):
        self.id = id
        self.uid = uid
        # ws:webscokethandle 的实例对象
        self.ws = ws
        self.sinIn = False
        self.messageCache=[]
        self.createTime = time.time()

    def setSinIn(self,flag):
        """
            flag:boolean
        """
        self.sinIn = flag
    def updateWs(self,ws):
        self.ws = ws

    @gen.coroutine
    def sendText(self,msg):
        ret = yield self.ws.replyText(msg)
        if not ret:
            self.messageCache.append(msg)


class Sessions:
    def __init__(self):
        self.uidContainer = {}
        self.socketContainer = {}
        self._nextSessionID = 0
    def listAll(self):
        items = []
        for _,session in self.uidContainer.items():
            item = {}
            item["id"] = session.id
            item["uid"] = session.uid
            item["createTime"] = session.createTime
            #item["messageCache"] = session.messageCache
            item["sinIn"] = session.sinIn
            items.append(item)
        return items

    def checkLogin(self,uid):
        session = self.uidContainer.get(uid,None)
        if not session:
            return False
        return session.sinIn

    def sinIn(self,uid):
        session = self.uidContainer.get(uid,None)
        if not session:
            return False
        session.setSinIn(True)
        return True

    def sinUp(self,uid):
        session = self.uidContainer.get(uid,None)
        if not session:
            return False
        session.setSinIn(True)
        return True

    def createNewSession(self,uid,ws):
        self._nextSessionID +=1
        nextSessionID = self._nextSessionID
        session = Session(nextSessionID,uid,ws)

        self.uidContainer[uid]= session
        self.socketContainer[ws] = session
        return session
    
    def removeSessionByUid(self,uid):
        if uid in self.uidContainer:
            del self.uidContainer[uid]

    def removeSessionBySocket(self,ws):
        if ws in self.socketContainer:
            del self.socketContainer[ws]

    def updateSessionByUid(self,uid,ws):
        self.uidContainer[uid].updateWs(ws)
 
    def findSessionByUid(self,uid):
        return self.uidContainer.get(uid,None)

    def findSessionByWs(self,ws):
        return self.socketContainer.get(ws,None)     

    @property
    def nextSessionID(self):
        self._nextSessionID +=1
        return self._nextSessionID
    
session = Session()