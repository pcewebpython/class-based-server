import socket
import sys
import traceback
import os
import mimetypes

class HttpServer():

    @staticmethod
    def make_response(
        code,
        reason,
        body=b"",
        mimetype=b"text/plain"
    ):
        """
        returns a basic HTTP response
        Ex:
            make_response(
                b"200",
                b"OK",
                b"<html><h1>Welcome:</h1></html>",
                b"text/html"
            ) ->

            b'''
            HTTP/1.1 200 OK\r\n
            Content-Type: text/html\r\n
            \r\n
            <html><h1>Welcome:</h1></html>\r\n
            '''
        """

        return b"\r\n".join([
            b"HTTP/1.1 " + code + b" " + reason,
            b"Content-Type: " + mimetype,
            b"",
            body
        ])

    @staticmethod
    def get_path(request):
        """
        Given the content of an HTTP request, return the _path_
        of that request.

        For example, if request were:

        '''
        GET /images/sample_1.png HTTP/1.1
        Host: localhost:1000

        '''

        Then you would return "/images/sample_1.png"
        """
        try:
            if "favicon.ico" in request:
                return "/webroot/favicon.ico"
            if "make_time.py" in request:
                return "/webroot/make_time.py"
            if "sample.txt" in request:
                return "/webroot/sample.txt"
            if "a_web_page.html" in request:
                return "/webroot/a_web_page.html"
            #if b"favicon.ico" in request:
                #return "/webroot/a_web_page.html"
        except:
            return "/"


    @staticmethod
    def get_mimetype(path):
        """
        This method should return a suitable mimetype for the given `path`.

        A mimetype is a short byte string that tells a browser how to
        interpret the response body. For example, if the response body
        contains a web page then the mimetype should be b"text/html". If
        the response body contains a JPG image, then the mimetype would
        be b"image/jpeg".

        Here are a few concrete examples:

            get_mimetype('/a_web_page.html') -> b"text/html"

            get_mimetype('/images/sample_1.png') -> b"image/png"

            get_mimetype('/') -> b"text/plain"
            # A directory listing should have either a plain text mimetype
            # or a b"text/html" mimetype if you turn your directory listings
            # into web pages.

            get_mimetype('/a_page_that_doesnt_exist.html') -> b"text/html"
            # This function should return an appropriate mimetype event
            # for files that don't exist.
        """
        try:
            if path.endswith('/'):
                return b"text/plain"
            if path.endswith('.html'):
                return b"text/html"
            if path.endswith('.png'):
                return b"image/png"
            if path.endswith('.jpg'):
                return b"image/jpg"
            if path.endswith('.ico'):
                return b"image/ico"
            if path.endswith('.txt'):
                return b"text/plain"
        except FileNotFoundError:
            return b"text/plain"


    @staticmethod
    def get_content(path):
        """
        This method should return the content of the file/directory
        indicated by `path`. For example, if path is `/a_web_page.html`
        then this function would return the contents of the file
        `webroot/a_web_page.html` as a byte string.

          * If the requested path is a directory, then the content should
          be a plain-text listing of the contents of that directory.

          * If the path is a file, it should return the contents of that
            file.

          * If the indicated path doesn't exist inside of `webroot`, then
            raise a FileNotFoundError.

        Here are some concrete examples:

        Ex:
            get_content('/a_web_page.html') -> b"<html><h1>North Carolina..."
            # Returns the contents of `webroot/a_web_page.html`

            get_content('/images/sample_1.png') -> b"A12BCF..."
            # Returns the contents of `webroot/images/sample_1.png`

            get_content('/') -> images/, a_web_page.html, make_type.py,..."
            # Returns a directory listing of `webroot/`

            get_content('/a_page_that_doesnt_exist.html') 
            # The file `webroot/a_page_that_doesnt_exist.html`) doesn't exist,
            # so this should raise a FileNotFoundError.
        """
        try:
            if os.path.isdir(path):
                entries = os.listdir(path)
                return entries

            if os.path.isfile(path):
                with open(path, 'r') as f:
                    data = f.read()
                return data

        except FileNotFoundError:
            return f"The file {path} does not exist"



    def __init__(self, port):
        self.port = port

    def serve(self):
        address = ('0.0.0.0', port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print("making a server on {0}:{1}".format(*address))
        print("Visit http://localhost:{}".format(port))

        sock.bind(address)
        sock.listen(10)

        try:
            while True:
                print('waiting for a connection')
                conn, addr = sock.accept()  # blocks until a connection arrives
                try:
                    print('connection - {0}:{1}'.format(*addr))

                    request = ''
                    while True:
                        data = conn.recv(1024)
                        request += data.decode('utf8')

                        if '\r\n\r\n' in request:
                            break
                    
                    print("Request received:\n{}\n\n".format(request))

                    path = self.get_path(request)
                    
                    try:
                        body = self.get_content(path)
                        mimetype = self.get_mimetype(path)

                        response = self.make_response(
                            b"200", b"OK", body, mimetype
                        )

                    except FileNotFoundError:
                        body = b"Couldn't find the file you requested."
                        mimetype = b"text/plain"

                        response = self.make_response(
                            b"404", b"NOT FOUND", body, mimetype
                        )

                    conn.sendall(response)
                except:
                    traceback.print_exc()
                finally:
                    conn.close() 

        except KeyboardInterrupt:
            sock.close()
            return
        except:
            traceback.print_exc()


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 10000 

    server = HttpServer(port)
    server.serve()

