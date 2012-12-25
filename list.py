import cgi
import datetime
import urllib
import webapp2
import json
import os

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template

class Main(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path,None))

class Item(db.Model):
  name = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

def shoppinglist_key():
  return db.Key.from_path('List','shoppinglist')

class IndexItems(webapp2.RequestHandler):
  def get(self):
    items = db.GqlQuery("SELECT * "
                        "FROM Item "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY date",
                        shoppinglist_key())
    names = []
    for item in items:
      names.append({
        'name':item.name
        ,'key':item.key().name()
        })

    self.response.out.write(json.dumps(names))


class AddItem(webapp2.RequestHandler):
  def post(self):
    name = self.request.get('name')
    item = Item(parent=shoppinglist_key(),key_name=name)
    item.name = name
    item.put()

class DeleteItem(webapp2.RequestHandler):
  def post(self):
    name = self.request.get('name')
    key = db.Key.from_path('List','shoppinglist','Item',name)
    db.delete(key)
   

app = webapp2.WSGIApplication([
                               ('/index', Main),
                               ('/rest/item/index', IndexItems),
                               ('/rest/item/add', AddItem),
                               ('/rest/item/delete', DeleteItem)
                              ], debug=True)
