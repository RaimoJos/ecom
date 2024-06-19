import logging
import ssl

from django.core.management.base import BaseCommand
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler
from django.core.wsgi import get_wsgi_application
from django.utils.autoreload import run_with_reloader

logging.basicConfig(level=logging.DEBUG)


class SSLWSGIServer(WSGIServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='ssl/cert.pem', keyfile='ssl/key.pem')
        self.socket = context.wrap_socket(self.socket, server_side=True)
        logging.debug("SSLWSGIServer initialized with SSL context")


class Command(BaseCommand):
    help = 'Run a development server with SSL.'

    def add_arguments(self, parser):
        parser.add_argument('addr', nargs='?', default='127.0.0.1', help='Optional IP address to bind to.')
        parser.add_argument('port', nargs='?', type=int, default=8000, help='Optional port number, defaults to 8000.')

    def handle(self, *args, **options):
        addr = options['addr']
        port = options['port']
        self.stdout.write(f"Starting development server at https://{addr}:{port}\n")
        self.stdout.write("Using SSL certificate from ssl/cert.pem and ssl/key.pem\n")

        def inner_run():
            handler = get_wsgi_application()
            logging.debug("WSGI application loaded")

            server_address = (addr, port)
            httpd = SSLWSGIServer(server_address, WSGIRequestHandler)
            httpd.set_app(handler)
            logging.debug("SSLWSGIServer ready to serve")

            httpd.serve_forever()

        run_with_reloader(inner_run)
