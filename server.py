#!/usr/env python3

import http.server as server
import re
import socketserver
import time
import urllib
import urllib.request as request

from template import get_page

team_pages = {}
host = "igem.org"
served_at = "localhost:8000"


def request_igem_file(path, sub_domain):
    resp = request.urlopen("http://" + sub_domain + host + "/" + path)
    data = resp.read()
    data = data.replace(host.encode("utf-8"), served_at.encode("utf-8"))
    return data, resp


def get_wiki_template(team, sub_domain):
    if team not in team_pages:
        try:
            data = re.split(r"<p>\W*IDE\W*</p>", request_igem_file(
                "Team:" + team + "/IDE",
                sub_domain
            )[0].decode('utf-8'))
            if len(data) != 2:
                return None
            team_pages[team] = data
        except request.HTTPError:
            return None
    return team_pages[team]


class IGEMHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path.startswith("/Team:"):
            sub_domain = self.headers["host"].replace(served_at, "")
            team = self.path[6:].split('/')[0]
            template = get_wiki_template(team, sub_domain)
            if template is None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(
                    "Please create an IDE template".encode('utf-8'))
                return
            self.send_response(200)
            self.end_headers()
            page = self.path[1:].split('/', 1)
            if len(page) == 1:
                page = ''
            else:
                page = '/' + page[1]
            template_head = template[0].replace('/IDE', page)
            template_foot = template[1].replace('/IDE', page)
            if page == "":
                page = "/"
            if page.endswith('/'):
                page += "index"
            self.wfile.write(template_head.encode('utf-8'))
            try:
                self.wfile.write(get_page(page).encode('utf-8'))
            except Exception as e:
                self.wfile.write(("Error:<br />" + str(e)).encode('utf-8'))
            self.wfile.write(template_foot.encode('utf-8'))
            return
        return self.proxy_upstream()
        # return super().do_GET()

    def do_POST(self):
        self.proxy_upstream()

    def proxy_upstream(self):
        head = self.headers
        nhost = head["Host"].replace(served_at, host)
        head["Host"] = nhost
        del head["Origin"]
        data = None
        if self.command == "POST":
            data = self.rfile.read(int(self.headers['Content-Length']))
        req = request.Request("http://" + nhost + self.path,
                              data=data,
                              headers=head,
                              method=self.command)
        try:
            with request.urlopen(req) as resp:
                self.send_response(resp.status)
                for k, v in dict(resp.info()).items():
                    if k not in ["Transfer-Encoding"]:
                        self.send_header(k, v.replace(host, served_at))
                self.end_headers()
                self.wfile.write(
                    resp.read().replace(
                        host.encode('utf-8'),
                        served_at.encode('utf-8')
                    ).replace(b"https", b"http")
                )
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()


class ThreadSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    Handler = IGEMHTTPRequestHandler
    stop = False
    while not stop:
        try:
            server = ThreadSocketServer(("0.0.0.0", 8000), Handler)
        except OSError as e:
            if e.errno != 98:
                raise
            print("Failed to listen, waiting 10 seconds")
            time.sleep(10)
        else:
            print("Now listening")
            stop = True
            server.allow_reuse_address = True
            server.serve_forever()
