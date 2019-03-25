from tornado import gen
from dbhelp.dbhelper import callPro,excuteSql
from base.messages import Message,ErrorCodes
import hashlib   

@gen.coroutine
def loginHandle(sessions,db_pool,msg):

    command = msg["login"]
    pwd = command["pwd"]
    p_type = msg["sender"]["type"]
    p_uid = command["uid"]
    m2 = hashlib.md5()
    m2.update((pwd.encode('utf-8')))
    p_pwd = m2.hexdigest()
    
    result = yield callPro(db_pool,'checkLogin',(p_type,p_uid,p_pwd))
    
    session = sessions.findSessionByUid(p_uid)
    response = {}

    if result.error and not result.next():

        error = Message.errorMsg(ErrorCodes.excuteSqlFailed)
        response = Message.buildResponseFromMsg(msg,'error',error)
    else:
        ret = result.next()
    
        check_login = result.value('checkLogin')
        #登陆成功
        if not check_login:
            sessions.sinUp(p_uid)
            okay = {"uid":p_uid,"sessionID":session.id}
            response = Message.buildResponseFromMsg(msg,'session',okay,session.id)
        #登陆失败
        else:
            error = Message.errorMsg(ErrorCodes.illegalUid)
            response = Message.buildResponseFromMsg(msg,'error',error)
    
    session.sendText(response)
    return True

@gen.coroutine
def getLineNetInfoHanle(sessions,db_pool,msg):

    command = msg["getLineNetInfo"]
    
    
    return True