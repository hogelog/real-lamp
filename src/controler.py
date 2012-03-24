'''
Created on 2012/03/20

@author: hogelog
'''

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import threading
import logging


class HttpControlerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        mapping = self.mapping()
        path = self.path
        if path in mapping:
            content = mapping[path]()
            if content:
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(500, "Server Error")
                self.end_headers()
        else:
            self.send_error(404, "Not Found")
            self.end_headers()

    def mapping(self):
        return {}


class BaseHttpControlerHandler(HttpControlerHandler):
    def index(self):
        return "Hello Http Controler!"

    def mapping(self):
        return {
            "/": self.index,
        }


class HttpControler(threading.Thread, HTTPServer):
    def __init__(self, host, port, handler):
        self.address = (host, port)
        self.handler = handler
        threading.Thread.__init__(self)
        HTTPServer.__init__(self, self.address, self.handler)

    def run(self):
        logging.info("start server: %s", self.address)
        self.serve_forever()

    def __stop(self):
        threading.Thread.__stop(self)
        logging.info("stop server: %s", self.address)

if __name__ == '__main__':
    class Handler(BaseHttpControlerHandler):
        def start(self):
            return "Start!"

        def stop(self):
            return "Stop!"

        def mapping(self):
            mapping = BaseHttpControlerHandler.mapping(self)
            mapping["/start"] = self.start
            mapping["/stop"] = self.stop
            return mapping

    server = HttpControler("0.0.0.0", 12345, Handler)
    server.start()
#    server.shutdown()
