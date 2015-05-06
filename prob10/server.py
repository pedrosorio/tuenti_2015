#!/usr/bin/env python

# this is an optimized HTTP server app
# we avoid re reading config on sub sequent requests by using a nice trick

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urlparse
import json
import cgi
import time
import Cookie
import hashlib
import urllib
import MySQLdb

CONFIG_FILE="hsl.config"

class HSLRequestHandler(BaseHTTPRequestHandler):
  def __init__(self, *args):
    self._load_templates()
    self.secret = self._get_secret()
    print self.secret
    BaseHTTPRequestHandler.__init__(self, *args)

  # Disable logging DNS lookups
  def address_string(self):
    return str(self.client_address[0])

  def _load_templates(self):
    self.template_files = {'login_form': 'templates/login_form.html',
                           'show_key': 'templates/show_key.html',
                           'invalid_credentials': 'templates/invalid_credentials.html'}
    self.templates = {}
    for k,v in self.template_files.iteritems():
      self.templates[k] = open(v, "r").read()

  def _get_secret(self):
    secret_file = '/etc/passwd'
    # 1992-04-08: cool secret store
    # we are assuming first line contains the root pass :)
    # TODO: review after the shadow password suite from J. Haugh is ported to Linux
    return "x"


class Handler(HSLRequestHandler):

    def do_GET(self):
        self.send_response(200)
        config = self._get_config_from_cookie(self.headers)
        if config:
          parsed_config = self._parse_config(config)
          print parsed_config
        else:
          config = self._get_config_from_file(CONFIG_FILE)

          cookie = Cookie.SimpleCookie()
          cookie['config'] = urllib.quote(config)
          cookie['sig'] = self._generate_sig(urllib.quote(config))
          for v in cookie.values():
            self.send_header('Set-Cookie', v.output(header='').lstrip())
        self.end_headers()

        message = self.templates['login_form']

        self.wfile.write(message)
        self.wfile.write('\n')
        return
    def do_POST(self):
      self.send_response(200)
      self.end_headers()
      length = int(self.headers.getheader('content-length'))

      parsed_config = None

      config = self._get_config_from_cookie(self.headers)
      if config:
        parsed_config = self._parse_config(config)
        print parsed_config
      else:
        config = self._get_config_from_file(CONFIG_FILE)

        cookie = Cookie.SimpleCookie()
        cookie['config'] = urllib.quote(config)
        cookie['sig'] = self._generate_sig(urllib.quote(config))
        for v in cookie.values():
          self.send_header('Set-Cookie', v.output(header='').lstrip())
      self.end_headers()

      postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)

      if 'user' in postvars and 'password' in postvars:
        authenticated = self._auth(parsed_config, postvars['user'][0], postvars['password'][0])

        if authenticated:
          message = self.templates['show_key']
        else:
          message = self.templates['invalid_credentials']

      else:
        message = 'you missed something'

      self.wfile.write(message)
      self.wfile.write('\n')
      return


    def _get_config_from_cookie(self, headers):
      if headers.has_key('cookie'):
        cookie = Cookie.SimpleCookie(headers.getheader("cookie"))
        config = cookie.get("config")
        sig = cookie.get("sig")
        if self._generate_sig(config.value) != sig.value:
          return None
        else:
          return config.value

      else:
        return None


    def _generate_sig(self, data):
      data = data.lower()
      return hashlib.md5(self.secret + data).hexdigest()


    def _parse_config(self, config):
      return urlparse.parse_qs(urlparse.unquote(config))


    def _get_config_from_file(self, f):
      with open(f) as ff:
        return ff.read()[:-1]


    def _auth(self, parsed_config, user, password):
      db = MySQLdb.connect(host=parsed_config['db_host'][0],
                           user=parsed_config['db_user'][0],
                           passwd=parsed_config['db_passwd'][0],
                           db=parsed_config['db_name'][0])
      cur = db.cursor()
      cur.execute("select * from users where name=%(user)s and passwd=%(passwd)s", {'user': user, 'passwd': password})
      row = cur.fetchone()
      print row
      db.close()
      return row


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 5252), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()