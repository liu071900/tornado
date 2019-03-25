
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler



class BaseHttp(RequestHandler):
    def initialize(self):
        """Hook for subclass initialization. Called for each request.

        A dictionary passed as the third argument of a url spec will be
        supplied as keyword arguments to initialize().

        Example::

            class ProfileHandler(RequestHandler):
                def initialize(self, database):
                    self.database = database

                def get(self, username):
                    ...

            app = Application([
                (r'/user/(.*)', ProfileHandler, dict(database=database)),
                ])
        """
        

    def prepare(self):
        """Called at the beginning of a request before  `get`/`post`/etc.

        Override this method to perform common initialization regardless
        of the request method.

        Asynchronous support: Decorate this method with `.gen.coroutine`
        or `.return_future` to make it asynchronous (the
        `asynchronous` decorator cannot be used on `prepare`).
        If this method returns a `.Future` execution will not proceed
        until the `.Future` is done.

        .. versionadded:: 3.1
           Asynchronous support.
        """
        pass
       
    def on_finish(self):
        """Called after the end of a request.

        Override this method to perform cleanup, logging, etc.
        This method is a counterpart to `prepare`.  ``on_finish`` may
        not produce any output, as it is called after the response
        has been sent to the client.
        """
        pass

class BaseWebscoket(WebSocketHandler):

    

    def check_origin(self, origin):
         return True
    