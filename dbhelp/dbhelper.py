from tornado import gen
from tormysql.cursor import DictCursor

from dbhelp.querySet import QuerySet



@gen.coroutine
def callProWithTransaction(db_pool,pro_name,*arg):
    """
        调用需要启用事务的存储过程
    """
    pass

@gen.coroutine
def callPro(db_pool,pro_name,*arg):
    """
        调用普通的存储过程，不需要事务
    """
    print('call {0} {1}'.format(pro_name,str(arg)) )

    ret = QuerySet()
    try:
        with (yield db_pool.Connection()) as conn:
            with conn.cursor(DictCursor) as cursor:
                yield cursor.callproc(pro_name,*arg)

                while cursor._cursor._result.has_next:
                    ret.put(cursor.fetchall()) 
                    yield cursor.nextset()
    except Exception as e:
        ret.setExcuteError(str(e.args))
    return ret
    
@gen.coroutine
def excuteSql(db_pool,sql):
    """ 
        执行不需要事务的sql语句
    """
    with (yield db_pool.Connection()) as conn:
        with conn.cursor(DictCursor) as cursor:
            yield cursor.execute('call getLayout(0,0)')
            datas = cursor.fetchall()
    return datas

@gen.coroutine
def excuteSqlWithTransaction(db_pool,sql):
    """ 
        执行 需要事务,的sql语句
    """
    pass