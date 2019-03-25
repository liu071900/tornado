from tornado import gen
from handles import dataHandle

handlesMap={
"login":dataHandle.loginHandle,
"getLineNetInfo":dataHandle.getLineNetInfoHanle

}


class Dispatcher:
    def __init__(self,handlesMap):
        self.handlesMap = handlesMap

    @gen.coroutine
    def dispatch(self,sessions,db_pool,msg):
        command = msg.get('command',None)
        handle = self.handlesMap.get(command,None)
        if not handle:
            return False
        results = yield handle(sessions,db_pool,msg)
        return results
    
dispatcher = Dispatcher(handlesMap)