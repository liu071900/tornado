from tornado.web import url
import handles
from handles.index import IndexHandle

routeMap = [
    url(r"/", 'handles.index.IndexHandle', name="index"),
    url(r"/dis/", 'handles.index.WsHandle', name="dis")
]

