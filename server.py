from http.server import HTTPServer, BaseHTTPRequestHandler
from time import strftime
log = []

class CS2610Assn1(BaseHTTPRequestHandler):
    """
    Your task is to define this class such that it fulfills the assingment
    requirements.

    Refer to the official Python documentation for the `http.server` class for
    details on what can go in here.

    Replace this pass statement with your own code:
    """

    def serve_file(self, fname, contentType='text/html'):
        f = open(fname, 'rb')
        data = f.read()
        f.close()

        self.wfile.write(b'HTTP/1.1 200 Ok\n')
        self.wfile.write(b"Server: Peter's Even Cooler Server\n")
        self.wfile.write(bytes(f"Date: {strftime('%c')}\n", 'utf-8'))
        self.wfile.write(b"Connection: close\n")
        self.wfile.write(b"Cache-Control: max-age=0.01\n")

        # this line gives the correct content-length
        self.wfile.write(bytes(f"Content-Length: {len(data)}\n", 'utf-8'))

        # instead of hard-coding the MIME type 'text/html', I should
        # look up the correct one for this filename
        self.wfile.write(bytes(f"Content-Type: {contentType}\n", 'utf-8'))
        self.wfile.write(b"\n")
        self.wfile.write(data)


    def redir301(self, location='/index.html'):
        self.wfile.write(b'HTTP/1.1 301 Moved Permanently\n')
        self.wfile.write(b"Server: Peter's Even Cooler Server\n")
        self.wfile.write(bytes(f"Date: {strftime('%c')}\n", 'utf-8'))
        self.wfile.write(bytes(f"Location: {location}\n", 'utf-8'))
        self.wfile.write(b"\n")


    def do_GET(self):
        print(f"GET {self.path}")
        log.append(f"GET {self.path}")
        if self.path == '/index.html':
            self.serve_file('index.html')

        elif self.path == '/style.css':
            self.serve_file('style.css', 'text/css')

        elif self.path == '/techtips.html':
            self.serve_file('techtips.html')

 
        elif self.path.startswith('/bio'):
            self.redir301("/about.html")

        elif self.path.startswith('/level'):
            n = int(self.path[6:])
            n += 1
            newLocation = f"/level{n}"
            self.redir301(newLocation)

        elif self.path == '/about.html':
            self.serve_file('about.html')

        elif self.path == '/Client.png':
            self.serve_file('Client.png', 'image/png')

        elif self.path == '/jeff.jpeg':
            self.serve_file('jeff.jpeg', 'image/jpeg')

        elif self.path == '/bike.jpeg':
            self.serve_file('bike.jpeg', 'image/jpeg')

        elif self.path == '/pizza.jpeg':
            self.serve_file('pizza.jpeg', 'image/jpeg')
 
        elif self.path == '/about':
            self.redir301()

        elif self.path == '/Client':
            self.redir301('/Client.png')

        elif self.path == '/jeff':
            self.redir301('/jeff.jpeg')

        elif self.path == '/bike':
            self.redir301('/bike.png')

        elif self.path == '/pizza':
            self.redir301('/pizza.png')

        elif self.path == '/' or self.path == '':
            self.redir301('/index.html')

        elif self.path == '/help':
            self.redir301('/techtips.html')

        elif self.path =='/teapot':
            resp = bytes(f"""
HTTP/1.1 418 I'm a Teapot
Server: Peter's Even Cooler Server
Date: {strftime('%c')}
Connection: close
Cache-Control: max-age=0.01

<html>
    <head>
        <title>Teapot.exe</title>
    </head>
    <body>
        <h1>This page is short and stout</h1>
        <p> <a href = /index.html> Click me to head to the main page </a></p>
    </body>
</html>
""", 'utf-8')
            self.wfile.write(resp)

        elif self.path == '/favicon.ico':
            self.serve_file('favicon.ico', 'image/ico')

        elif self.path == '/forbidden':
            resp = bytes(f"""
HTTP/1.1 403 Forbidden
Server: Peter's Even Cooler Server
Date: {strftime('%c')}
Connection: close
Cache-Control: max-age=0.01

<html>
    <head>
        <title>Get out</title>
    </head>
    <body>
        <h1>You are not allowed to access this page</h1>
        <p> <a href = /index.html> Click me to head to the main page </a></p>
    </body>
</html>
""", 'utf-8')
            self.wfile.write(resp)

        elif self.path == '/debugging':
            resp = bytes(f"""
HTTP/1.1 200 OK
Server: Peter's Even Cooler Server
Date: {strftime('%c')}
Connection: close
Cache-Control: max-age=0.01

<html>
    <head>
        <link rel="stylesheet" href="style.css" type="text/css"/>
        <title>debugger</title>
    </head>
    <body>
        <h1>Debugging page</h1>
        <p> <a href = /index.html> Click me to head to the main page </a></p>
        <p>version: {self.version_string()}</p>
        <p>time: {strftime('%c')} </p>
        <p>ip-address: {self.client_address[0]}</p>
        <p>port number: {self.client_address[1]}</p>
        <p>path: {self.path} </p>
        <p>command: {self.command} </p>
        <p>request version: {self.request_version}</p>
        <ol>{generateLog(log)}<ol>
    </body>
</html>
""", 'utf-8')
            self.wfile.write(resp)

        else:
            resp = bytes(f"""
HTTP/1.1 404 Not Found
Server: Peter's Even Cooler Server
Date: {strftime('%c')} 
Connection: close
Cache-Control: max-age=0.01

<html>
    <head>
        <title>File does not exist</title>
    </head>
    <body>
        <h1>That file doesn't exist</h1>
        <p>Please try again when you can learn to spel</p>
    </body>
</html>
""", 'utf-8')
            self.wfile.write(resp)


def generateLog(l):
    toReturn = ""
    for i in l:
        toReturn += "<li>" + str(i) + "</li>"
    return toReturn

if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    HTTPServer(server_address, CS2610Assn1).serve_forever()
