import os.path
import re
import tornado.web
import tornado.wsgi
import unicodedata

from google.appengine.ext import db
from utils import wget


class Entry(db.Model):
    """A single word entry."""
    word_hash = db.StringProperty(required=True)
    word_encrypt = db.StringProperty(required=True)
    word_freq = db.IntegerProperty(required=True)

class HomeHandler(tornado.web.RequestHandler):
    """Displays the home page."""
    def get(self):
        self.render("index.html", )

class URLHandler(tornado.web.RequestHandler):
    """Handles the request and returns the data."""
    def get(self):
        # Redirect to home.html
        self.render("index.html", )

    def post(self):
        url = self.get_argument("url", default=None, strip=False)
        response = 'Nothing yet'

        response = wget(url).replace('\n','')
            
        self.render("word.html", url=url, results=response)

def handle_request(response):
    '''Callback needed when a response arrives.'''
    if response.error:
        print "Error:", response.error
    else:
        print 'called'
        print response.body

settings = {
    #"blog_title": u"Tornado Blog",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    #"ui_modules": {"Entry": EntryModule},
    #"xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/word", URLHandler),
    (r"/.*", HomeHandler),
], **settings)

application = tornado.wsgi.WSGIAdapter(application)
