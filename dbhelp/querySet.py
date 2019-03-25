

class QuerySet():
    """
        查询结果存放集，按照sql返回的结果集顺序存放，顺序获取
    """
    def __init__(self):
        self._set = {}
        self._set[0]= 0
        self._next_key = 0
        self._put_key = 1
    
    def next(self):
        """
            从QuerySet 里取下一个结果集，如果没有更多结果集返回 None
        """
        self._next_key += 1
        key = self._next_key
        return self._set.get(key,None)

    def value(self,v):
        """
            从当前结果集里取给定字段的值
        """
        key = self._next_key

        d = self._set[key][0]
        
        return d.get(v,None)

    def put(self,result):
        """
            存放结果集到 QuerySet
        """
        key = self._put_key
        self._set[key] = result
        self._put_key += 1
    
    def setExcuteError(self,e):
        """
            存放error信息到 QuerySet
        """
        self._set[0] = e
    
    @property
    def error(self):
        """
            查询结果的error信息
        """
        return self._set[0]