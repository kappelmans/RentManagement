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
<div><p>Gateway 1111111111111111111 Serial</p><input type="text" name="gateway_serial"></div>
<div><p>ReadOut</p><input type="text" name="readout"></div>
      <div>
      <input type="submit" value="POST RESULT">
      </div>
      
    </form>
  </body>
</html>
"""

class DoUpload(webapp2.RequestHandler):
  def post(self):
      fl = self.request.get('myfile')
      for contr in Contract.all():
          contr.delete()
      for prop in Property.all():
          prop.delete()
      for addr in Address.all():
          addr.delete()
      for pers in Person.all():
          pers.delete()
          
      self.response.write(fl.decode("latin-1")+"<br/>Hallo Kris<br/>" )
      reader = csv.reader(fl.decode("latin-1").splitlines(), delimiter=";")
      rownum = 0
      for row in reader:
         if (rownum > 0 ):
            self.response.write(row[0] + "<br/>")   
            addr = Address(street= row[2], postalCode = row[3], locality = row[4])
            addr.put()
            prop = Property(shortName = row[0], propertyType=int(row[1]), propertyOwner=int(row[5]), address=addr.key() )
            prop.put()
            pers = Person(name=row[6], language=row[8], aanspreekTittel =row[7])
            if row[15] != None and len(row[15])>1:
                addr = Address(street= row[15], postalCode = row[16], locality = row[17])
                addr.put()
                pers.address = addr.key()
            pers.put()
            contr = Contract(tenant = pers.key(), property= prop.key(), startDate = datetime.strptime(row[13],"%d/%m/%Y") , baseIndex=float(row[9]), baseIndexType=int(row[10]), baseRent=float(row[11]), provision=float(row[12]), indexMonth=int(row[14]))
            if row[15] != None and len(row[15])>1:
                contr.useTenantAddress = bool(True)
            else:   
                contr.useTenantAddress = bool(False)

            contr.put()
         rownum += 1   

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)      
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/uploadFile.do', DoUpload)
], debug=True)

