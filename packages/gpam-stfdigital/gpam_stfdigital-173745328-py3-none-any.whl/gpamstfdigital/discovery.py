import os
import socketserver
import json

from threading import Thread
from consul import Consul
from http.server import SimpleHTTPRequestHandler

class HealthServer(SimpleHTTPRequestHandler):
    def do_GET(self):   
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        self.wfile.write(bytes(json.dumps({"status":"ok"}), 'utf8'))

        return json.dumps({"status" :"OK"})

class Discovery:

    def __init__(self, host, port):

        self._client = Consul(host=host,
                              port=port)

    @staticmethod
    def parse_health(host, port, endpoint, interval=10):
        """
        Return a dict with health checking information 
        """

        url = os.path.join(host + ':' + str(port), endpoint)

        return Check.http(url, interval)

    def _verify_service_registered(self, app_name):
        """
        Verify is consul service is running
        """

        # TODO view if app_name is registered and 
        checks = self._client.health.checks(app_name)[1]

        return checks != []

    def register_app(self, app_name, port):
        """
        Register a app with service_id equal of app_name, in a consul
        agent it's impossible use the same service_id take care of it.
        """

        response = self._client.agent.service.register(app_name)

        return response 

    @staticmethod
    def up_http_server(host, port, endpoint='/manage/health'):
        """
        Create a child thread with http server registered in 
        host:port 
        """

        httpd = socketserver.TCPServer((host, port), HealthServer)
        httpd.path = endpoint

        server_thread = Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        
    def remove_app(self, service_id):
        """
        Remove a app from catalog and return a boolean
        """

        response = self._client.agent.service.deregister(service_id)

        return response

    def search_app(self, app_name):
        pass
