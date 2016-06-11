# Core Handler
# Fetches the URL and return the top 100 words

import os.path
import re
import tornado.web
import tornado.wsgi
import unicodedata

from google.appengine.ext import db


class Entry(db.Model):
    """A single word entry."""
    word_hash = db.StringProperty(required=True)
    word_encrypt = db.StringProperty(required=True)
    word_freq = db.IntegerProperty(required=True)

class URLHandler(tornado.web.RequestHandler):
    """Handles the request and returns the data."""
    def get(self):
        # Redirect to home.html
        self.redirect('/')

    def post(self):
        url = self.get_argument("url", default=None, strip=False)
        self.render("word.html", url=url)

settings = {
    #"blog_title": u"Tornado Blog",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    #"ui_modules": {"Entry": EntryModule},
    #"xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/word", URLHandler),
], **settings)

application = tornado.wsgi.WSGIAdapter(application)
