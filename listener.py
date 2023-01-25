from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import ssl
import json


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if "Content-Length" in self.headers:
            self.data_string = self.rfile.read(int(self.headers["Content-Length"]))
        elif "chunked" in self.headers.get("Transfer-Encoding", ""):
            self.data_string = bytes()
            while True:
                line = self.rfile.readline().strip()
                chunk_length = int(line, 16)
                if chunk_length != 0:
                    self.data_string += self.rfile.read(chunk_length)
                self.rfile.readline()
                if chunk_length == 0:
                    break
        self.send_response(200)
        self.end_headers()
        data = json.loads(self.data_string)
        data["Sender-Address"] = self.headers["Sender-Address"]
        print(data)
        return

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("", 4000), Handler)
    server.socket = ssl.wrap_socket(
        server.socket,
        ssl_version=ssl.PROTOCOL_TLS,
        keyfile="/etc/tls.key",
        certfile="/etc/tls.crt",
        server_side=True,
    )
    server.serve_forever()
