from tornado.web import Application

from tornado.platform.asyncio import AsyncIOMainLoop
#from tornado.ioloop import IOLoop
from tornado.ioloop import PeriodicCallback
from concurrent.futures import ThreadPoolExecutor

import uvloop
import asyncio

import tormysql

from base.routerMap import routeMap
from config.settings import app_settings,db_pool

from base.sessions import session
from base.dispatchers import dispatcher


class AfcApp(Application):
    def __init__(self,*arg,**kwg):
        super(AfcApp,self).__init__(*arg,**kwg)
        self.db_pool = db_pool
        self.dispatcher = dispatcher
        self.Sessions = session
        self.thread_executor = ThreadPoolExecutor(8)
        
    def start(self,port=8080):
        self.listen(port)

if __name__=='__main__':

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    AsyncIOMainLoop().install()
    loop = asyncio.get_event_loop()
    app = AfcApp(routeMap,**app_settings)

    app.start(8080)

    loop.run_forever()