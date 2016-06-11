import os.path
import re
import tornado.web
import tornado.wsgi
import unicodedata

from google.appengine.ext import db


class Entry(db.Model):
    """A single blog entry."""
    word_hash = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    body_source = db.TextProperty(required=True)
    html = db.TextProperty(required=True)
    published = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", )

settings = {
    #"blog_title": u"Tornado Blog",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    #"ui_modules": {"Entry": EntryModule},
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", HomeHandler),
], **settings)

application = tornado.wsgi.WSGIAdapter(application)
