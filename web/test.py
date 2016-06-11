import os.path
import tornado.web
import tornado.wsgi

class DisplayHandler(tornado.web.RequestHandler):
    """Displays the home page."""
    def get(self):
        self.render("index.html", )

settings = {
    #"blog_title": u"Tornado Blog",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    #"ui_modules": {"Entry": EntryModule},
    #"xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/.*", DisplayHandler),
], **settings)

application = tornado.wsgi.WSGIAdapter(application)
