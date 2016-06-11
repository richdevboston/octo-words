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

        # Fetch URL and extract content
        response = wget(url).replace('\r\n','').replace('\n', '')   # Fetch URL and remove newlines
        regex = re.compile('(?<=body).*?(?=<\/body>)')              # extract content of body HTML tag
        response = regex.findall(response)[0]                       
        response = re.sub(r'<.*?>', ' ', response)                  # Remove HTML tags

        # Remove prepositions and articles
        prep_arr = [
                'on', 'in', 'at', 'since', 'for', 'ago', 'before', 'to', 'until', 'till', 'by',
                'off', 'about', 'from', 'onto', 'unto', 'into', 'through', 'across', 
                'above', 'below', 'over', 'under', 'beside', 'next',
                'a', 'an', 'the', 'some', 'few', 'this', 'that', 'those', 'these'
                'how', 'why', 'what', 'who', 'when', 'there', ]
        for i in prep_arr:
            response = response.replace(i, '')

        # Create word dictionary and frequency
        wordcount = {}
        regex = re.compile('[a-zA-Z\-]{3,}')
        words = regex.findall(response)
        for word in words:
            if word not in wordcount:
                wordcount[word] = {'freq': 1, 'fontSize': 1}
            else:
                wordcount[word]['freq'] += 1

        # Sort words by frequency
        high = 0
        for word in wordcount:
            high = max(high, wordcount[word]['freq'])
        
        for word in wordcount:
            wordcount[word]['fontSize'] = float(wordcount[word]['freq']) / float(high) * float(400)
            
        self.render("word.html", url=url, results=wordcount)

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
