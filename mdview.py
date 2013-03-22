#!/usr/bin/env python

import os
import sys
import time
import random
import codecs
import markdown
import datetime
import webbrowser
import threading
import BaseHTTPServer
from optparse import OptionParser


def build_html_from_markdown(filespec):

    def markdown_as_html():
        input_file = codecs.open(filespec, mode="r", encoding="utf-8")
        text = input_file.read()
        input_file.close()
        #return markdown.markdown(text,extensions=['nl2br'],output_format="html5")
        return markdown.markdown(text,output_format="html5")

    def title():
        return '<title>md %s</title>\r\n' % os.path.basename(filespec)[:-3].split('.')[0]

    def javascript():
        return """
            <script type="text/javascript">
                function keep_alive() {
                    window.open("/tickle_myself","_self");
                }
                setInterval(keep_alive,1000)
            </script>
        """


    html = ( '<!DOCTYPE html>\r\n'
             '<html>\r\n'
             '<head>\r\n' )
    html += title()
    html += '<link rel="stylesheet" href="/mdview_stylesheet.css" type="text/css">\r\n'
    html += ( '</head>\r\n'
              '<body><div id="markdown-body">\r\n' )
    html += markdown_as_html()
    html += '</div>\r\n'
    html += javascript()
    html += '</body>\r\n</html>'

    return html

def stylesheet():
    # much of this matches https://gist.github.com/andyferra/2554919
    return """
    * {
        padding: 0;
        margin: 0;
    }
    body {
      font-family: Helvetica, arial, sans-serif;
      font-size: 14px;
      line-height: 1.6;
      padding-top: 10px;
      padding-bottom: 10px;
      background-color: white;
      padding: 30px; }

    body > *:first-child {
      margin-top: 0 !important; }
    body > *:last-child {
      margin-bottom: 0 !important; }

    a {
      color: #4183C4;
      text-decoration: none; }
    a.absent {
      color: #cc0000; }
    a.anchor {
      display: block;
      padding-left: 30px;
      margin-left: -30px;
      cursor: pointer;
      position: absolute;
      top: 0;
      left: 0;
      bottom: 0;
      text-decoration: none; }

    h1, h2, h3, h4, h5, h6 {
      margin: 20px 0 10px;
      padding: 0;
      font-weight: bold;
      -webkit-font-smoothing: antialiased;
      cursor: text;
      position: relative; }

    h1:hover a.anchor, h2:hover a.anchor, h3:hover a.anchor, h4:hover a.anchor, h5:hover a.anchor, h6:hover a.anchor {
      /*background: url("../../images/modules/styleguide/para.png") no-repeat 10px center; */
      text-decoration: none; }

    h1 tt, h1 code {
      font-size: inherit; }

    h2 tt, h2 code {
      font-size: inherit; }

    h3 tt, h3 code {
      font-size: inherit; }

    h4 tt, h4 code {
      font-size: inherit; }

    h5 tt, h5 code {
      font-size: inherit; }

    h6 tt, h6 code {
      font-size: inherit; }

    h1 {
      font-size: 28px;
      color: black; }

    h2 {
      font-size: 24px;
      border-bottom: 1px solid #cccccc;
      color: black; }

    h3 {
      font-size: 18px; }

    h4 {
      font-size: 16px; }

    h5 {
      font-size: 14px; }

    h6 {
      color: #777777;
      font-size: 14px; }

    p, blockquote, ul, ol, dl, li, table, pre {
      margin: 15px 0; }

    hr {
      /*background: transparent url("../../images/modules/pulls/dirty-shade.png") repeat-x 0 0;*/
      border: 0 none;
      color: #cccccc;
      height: 4px;
      padding: 0; }

    body > h2:first-child {
      margin-top: 0;
      padding-top: 0; }
    body > h1:first-child {
      margin-top: 0;
      padding-top: 0; }
      body > h1:first-child + h2 {
        margin-top: 0;
        padding-top: 0; }
    body > h3:first-child, body > h4:first-child, body > h5:first-child, body > h6:first-child {
      margin-top: 0;
      padding-top: 0; }

    a:first-child h1, a:first-child h2, a:first-child h3, a:first-child h4, a:first-child h5, a:first-child h6 {
      margin-top: 0;
      padding-top: 0; }

    h1 p, h2 p, h3 p, h4 p, h5 p, h6 p {
      margin-top: 0; }

    li p.first {
      display: inline-block; }

    ul, ol {
      padding-left: 30px; }

    ul :first-child, ol :first-child {
      margin-top: 0; }

    ul :last-child, ol :last-child {
      margin-bottom: 0; }

    dl {
      padding: 0; }
      dl dt {
        font-size: 14px;
        font-weight: bold;
        font-style: italic;
        padding: 0;
        margin: 15px 0 5px; }
        dl dt:first-child {
          padding: 0; }
        dl dt > :first-child {
          margin-top: 0; }
        dl dt > :last-child {
          margin-bottom: 0; }
      dl dd {
        margin: 0 0 15px;
        padding: 0 15px; }
        dl dd > :first-child {
          margin-top: 0; }
        dl dd > :last-child {
          margin-bottom: 0; }

    blockquote {
      border-left: 4px solid #dddddd;
      padding: 0 15px;
      color: #777777; }
      blockquote > :first-child {
        margin-top: 0; }
      blockquote > :last-child {
        margin-bottom: 0; }

    table {
      padding: 0; }
      table tr {
        border-top: 1px solid #cccccc;
        background-color: white;
        margin: 0;
        padding: 0; }
        table tr:nth-child(2n) {
          background-color: #f8f8f8; }
        table tr th {
          font-weight: bold;
          border: 1px solid #cccccc;
          text-align: left;
          margin: 0;
          padding: 6px 13px; }
        table tr td {
          border: 1px solid #cccccc;
          text-align: left;
          margin: 0;
          padding: 6px 13px; }
        table tr th :first-child, table tr td :first-child {
          margin-top: 0; }
        table tr th :last-child, table tr td :last-child {
          margin-bottom: 0; }

    img {
      max-width: 100%; }

    span.frame {
      display: block;
      overflow: hidden; }
      span.frame > span {
        border: 1px solid #dddddd;
        display: block;
        float: left;
        overflow: hidden;
        margin: 13px 0 0;
        padding: 7px;
        width: auto; }
      span.frame span img {
        display: block;
        float: left; }
      span.frame span span {
        clear: both;
        color: #333333;
        display: block;
        padding: 5px 0 0; }
    span.align-center {
      display: block;
      overflow: hidden;
      clear: both; }
      span.align-center > span {
        display: block;
        overflow: hidden;
        margin: 13px auto 0;
        text-align: center; }
      span.align-center span img {
        margin: 0 auto;
        text-align: center; }
    span.align-right {
      display: block;
      overflow: hidden;
      clear: both; }
      span.align-right > span {
        display: block;
        overflow: hidden;
        margin: 13px 0 0;
        text-align: right; }
      span.align-right span img {
        margin: 0;
        text-align: right; }
    span.float-left {
      display: block;
      margin-right: 13px;
      overflow: hidden;
      float: left; }
      span.float-left span {
        margin: 13px 0 0; }
    span.float-right {
      display: block;
      margin-left: 13px;
      overflow: hidden;
      float: right; }
      span.float-right > span {
        display: block;
        overflow: hidden;
        margin: 13px auto 0;
        text-align: right; }

    code, tt {
      margin: 0 2px;
      padding: 0 5px;
      white-space: nowrap;
      border: 1px solid #eaeaea;
      background-color: #f8f8f8;
      border-radius: 3px; }

    pre code {
      margin: 0;
      padding: 0;
      white-space: pre;
      border: none;
      background: transparent; }

    .highlight pre {
      background-color: #f8f8f8;
      border: 1px solid #cccccc;
      font-size: 13px;
      line-height: 19px;
      overflow: auto;
      padding: 6px 10px;
      border-radius: 3px; }

    pre {
      background-color: #f8f8f8;
      border: 1px solid #cccccc;
      font-size: 13px;
      line-height: 19px;
      overflow: auto;
      padding: 6px 10px;
      border-radius: 3px; }
      pre code, pre tt {
        background-color: transparent;
        border: none; }

    #markdown-body {
        border: 1px solid #CACACA;
        padding: 30px;
        margin: 10px
        width: 846px;
        max-width: 846px;
        margin-left: auto;
        margin-right: auto;
    }
    li {
      padding: 0;
      margin: 0;
    }
    hr {
        border-bottom: dashed 3px #ccc;
    }
    """


class http_md_handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.server.cfg.tickle_time = time.time()

        def nice_failure(message,code=200):
            self.send_response(code)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(message)

        try:

            if self.path == '/tickle_myself':
                self.send_response(204)
                self.end_headers()
                self.wfile.write('')
                if not self.server.cfg.quiet:
                    print '.',
                sys.stdout.flush()
            else:
                if not self.server.cfg.quiet:
                    print self.path
                if self.path == '/mdview_stylesheet.css':
                    almost_one_hour = datetime.datetime.utcnow() + datetime.timedelta(seconds=(60*60))
                    expires = almost_one_hour.strftime('%a, %d %b %Y 20:00:00 GMT')
                    self.send_response(200)
                    self.send_header("Content-type","text/css")
                    self.send_header("Expires",expires)
                    #self.send_header('Cache-Control','no-cache')
                    self.end_headers()
                    self.wfile.write(stylesheet())
                elif self.path == '/favicon.ico':
                    self.send_response(404)
                    almost_one_hour = datetime.datetime.utcnow() + datetime.timedelta(seconds=(60*60))
                    expires = almost_one_hour.strftime('%a, %d %b %Y 20:00:00 GMT')
                    self.send_header("Expires",expires)
                    self.end_headers()
                    self.wfile.write('')
                else:
                    filespec = os.path.normpath(self.server.cfg.file_base + self.path)

                    # file must be a markdown, and must be within file_base
                    if not filespec.startswith(self.server.cfg.file_base + os.sep):
                        nice_failure("Can only read files within " + self.server.cfg.file_base)
                    elif not (filespec.lower().endswith(".md") or filespec.lower().endswith(".markdown")):
                        nice_failure("Can only read .md or .markdown files, not " + self.path)
                    elif not os.path.exists(filespec):
                        nice_failure("file not found: " + filespec)
                    else:

                        self.send_response(200)
                        self.send_header("Content-type","text/html")
                        self.send_header('Cache-Control','no-cache')
                        self.end_headers()
                        self.wfile.write(build_html_from_markdown(filespec))

        except Exception, err:
            nice_failure("Error deliverying file" + str(err),404)

    def log_message(self,format,*args):
        # trick to suppress logs from http://stackoverflow.com/questions/3389305/how-to-silent-quiet-httpserver-and-basichttprequesthandlers-stderr-output
        return

class http_md_server(BaseHTTPServer.HTTPServer):

    def __init__(self,cfg,server_address,http_handler):
        BaseHTTPServer.HTTPServer.__init__(self,server_address,http_handler)
        self.cfg = cfg

def serve_markdown_on_some_available_port(cfg,first_file_url):

    # try opening on a bunch of ports until we find one that is available
    attempt = 0
    while True:
        try:
            port = int(cfg.port) if (cfg.port is not None) else random.randint(5000,9999)
            server_address = ('127.0.0.1', port)

            httpd = http_md_server(cfg, server_address, http_md_handler)
        except:
            attempt += 1
            if attempt == 1000:
                raise
        else:
            break

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    #httpd.serve_forever()
    cfg.tickle_time = time.time()
    threading.Thread(target=httpd.serve_forever).start()

    webbrowser.open_new_tab( "http://%s:%d/%s" % (server_address[0],server_address[1],first_file_url) )

    return httpd

def main():

    class config(object):
        def __init__(self,file_base,port,quiet,forever):
            self.file_base = file_base
            self.tickle_time = 0
            self.port = port
            self.quiet = quiet
            self.forever = forever

    parser = OptionParser(usage="usage: %prog filespec.md [options]")
    parser.add_option("-q","--quiet",action="store_true",dest="quiet",default=False,help="do not print messages on every request")
    parser.add_option("--forever",action="store_true",dest="forever",default=False,help="run server forever, even if browser stops requesting markdown files")
    parser.add_option("-p","--port",dest="port",help="server port (else will search for an available port)")

    (options,args) = parser.parse_args()

    if 1 < len(args):
        parser.error("Too many arguments.")
    if 0 == len(args):
        print "TRIVIAL MARKDOWN SERVER: view github-flavored markdown files locally"
        parser.print_help()
        print
        print "more at: https://github.com/BrentNoorda/trivial_markdown_server"
        return

    # only accept .markdown or .md files
    filespec = os.path.abspath(os.path.expanduser(args[0]))
    ext = os.path.splitext(filespec)[1]
    if ext.lower() not in ('.md','.markdown'):
        parser.error("Filespec must be markdown; i.e. .md or .markdown")

    cfg = config(os.path.normpath(os.path.split(filespec)[0]),options.port,options.quiet,options.forever);

    httpd = serve_markdown_on_some_available_port(cfg,filespec[len(cfg.file_base)+1:])

    try:
        while True:
            if not cfg.forever:
                tickle_age = time.time() - cfg.tickle_time
                if 4 < tickle_age:
                    # it has been more than 4 seconds since we heard from the client, so quit
                    break
            time.sleep(1)
    except:
        pass

    httpd.shutdown()

if __name__ == "__main__":
    main()
