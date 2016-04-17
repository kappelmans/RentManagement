import cgi
import os
from google.appengine.api import users
import webapp2
from google.appengine.ext import ndb
import json
from datetime import datetime
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/gwy/test_submitreading" method="post">
<div><p>Gateway Serial</p><input type="text" name="gateway_serial"></div>
<div><p>ReadOut</p><input type="text" name="readout"></div>
      <div>
      <input type="submit" value="POST RESULT">
      </div>
      
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)      
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    
    
], debug=True)