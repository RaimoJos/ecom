import ssl
from http.server import HTTPServer

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application


class SSLHTTPServer(HTTPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='ssl/cert.pem', keyfile='ssl/key.pem')
        self.socket = context.wrap_socket(self.socket, server_side=True)


class Command(BaseCommand):
    help = 'Run a development server with SSL.'

    def add_arguments(self, parser):
        parser.add_argument('addr', nargs='?', default='0.0.0.0', help='Optional IP address to bind to.')
        parser.add_argument('port', nargs='?', type=int, default=8000, help='Optional port number, defaults to 8000.')

    def handle(self, *args, **options):
        addr = options['addr']
        port = options['port']

        self.stdout.write(
            "Starting development server at https://{}:{}\n".format(addr, port)
        )
        self.stdout.write("Using SSL certificate from ssl/cert.pem and ssl/key.pem\n")

        handler = get_wsgi_application()
        httpd = SSLHTTPServer((addr, port), handler)
        httpd.serve_forever()


if __name__ == '__main__':
    settings.configure()
    application = get_wsgi_application()
    Command().handle(addr='0.0.0.0', port=8000)
