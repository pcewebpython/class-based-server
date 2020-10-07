import unittest
import os
from http_server import HttpServer


class TestCase(unittest.TestCase):

    def test_make_response(self):
        code = b"200"
        reason = b"OK"
        body = b"foo"
        mimetype = b"image/bmp"

        response = HttpServer.make_response(code, reason, body, mimetype)
        str_response = response.decode()

        self.assertIn("\r\n\r\n", str_response)

        str_header, str_body = str_response.split("\r\n\r\n")

        self.assertEqual(body.decode(), str_body)
        self.assertEqual("HTTP/1.1 200 OK",
                         str_header.splitlines()[0])
        self.assertIn("Content-Type: " + mimetype.decode(), str_header)

    def test_get_path(self):
        path = "/foo"
        request_head = "GET {} HTTP/1.1".format(path)

        self.assertEqual(path, HttpServer.get_path(request_head))

    def test_get_content_file(self):
        path = "/a_web_page.html"

        content = HttpServer.get_content(path)

        with open(os.path.join("webroot", "a_web_page.html"), "rb") as f:
            self.assertEqual(f.read(), content)

    def test_get_mimetype_file(self):
        path = "/a_web_page.html"

        mimetype = HttpServer.get_mimetype(path)

        self.assertEqual(b"text/html", mimetype)
        
    def test_get_content_dir(self):
        path = "/"

        content = HttpServer.get_content(path)

        self.assertIn(b"favicon.ico", content)
        self.assertIn(b"make_time.py", content)
        self.assertIn(b"sample.txt", content)
        self.assertIn(b"a_web_page.html", content)

    def test_get_mimetype_dir(self):
        path = "/foo/"

        mimetype = HttpServer.get_mimetype(path)

        self.assertIn(mimetype, [b"text/html", b"text/plain"])
        

    def test_get_content_not_found(self):
        path = "/foo/bar/baz/doesnt/exist"

        with self.assertRaises(FileNotFoundError):
            HttpServer.get_content(path)


if __name__ == '__main__':
    unittest.main()
