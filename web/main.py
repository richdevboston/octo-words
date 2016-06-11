import os.path
import re
import tornado.web
import tornado.wsgi
import unicodedata
import uuid
import hashlib

import MySQLdb 

from google.appengine.ext import db
##from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from utils import wget

CLOUDSQL_PROJECT = 'octo-words'
CLOUDSQL_INSTANCE = 'octo-words'
SALT = 'ba4ae64a7f60c7b13214a86ef2c59438'
ENCRYPT_KEY = '1c99a1de324e9a825f7e269f0c2a2f99'
IV = '\x04\x80_\xb5\x10H\r"\n}\xf1-\xd3\x85\x0c\x11'

class Entry(db.Model):
    """A single word entry."""
    word_hash = db.StringProperty(required=True)
    word_encrypt = db.StringProperty(required=True)
    word_freq = db.IntegerProperty(required=True)

class SQLHandler(tornado.web.RequestHandler):
    def get(self):
        db = MySQLdb.connect(
                unix_socket='/cloudsql/{}:{}'.format(CLOUDSQL_PROJECT, CLOUDSQL_INSTANCE),
                user='root',
                passwd='octo stuff is being setup',
                db='words')

        cursor = db.cursor()
        cursor.execute('SELECT * FROM entries')

        result = cursor.fetchall();
        #for r in cursor.fetchall():
        #    print('{}\n'.format(r))

        self.render("sql.html", results=result)

class HomeHandler(tornado.web.RequestHandler):
    """Displays the home page."""
    def get(self):
        self.render("index.html", )

    def post(self):
        url = self.get_argument("url", default=None, strip=False)
        if not url.startswith('http://'):
            url = 'http://' + url
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
                #wordcount[word] = {'freq': 1, 'fontSize': 1}
                wordcount[word] = 1
            else:
                wordcount[word] += 1

        # Find top 100 words
        tuples = sorted(wordcount.iteritems(), key=lambda (k,v):(v,k))
        tuples.reverse()
        count = 0
        wordcount = {}
        for i in tuples:
            wordcount[i[0]] = {'freq': i[1], 'fontSize': 1}
            count += 1
            if count >= 100:
                break

        # Find highest value
        high = 0
        for word in wordcount:
            high = max(high, wordcount[word]['freq'])
        
        # Define font size relative to the highest value
        for word in wordcount:
            wordcount[word]['fontSize'] = float(wordcount[word]['freq']) / float(high) * float(400)

        # Insert into DB
        db = MySQLdb.connect(
                unix_socket='/cloudsql/{}:{}'.format(CLOUDSQL_PROJECT, CLOUDSQL_INSTANCE),
                user='root',
                passwd='octo stuff is being setup',
                db='words')
        cursor = db.cursor()
        for word in wordcount:
            #salt = uuid.uuid4().hex
            hashed_word = hashlib.sha512(word + SALT).hexdigest()

            # Encryption
        #    encryption_suite = AES.new(ENCRYPT_KEY, AES.MODE_CBC, IV)
        #    cipher_text = encryption_suite.encrypt(word)

            # Decryption
            #decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
            #plain_text = decryption_suite.decrypt(cipher_text)

            #cursor.execute('select * from entries where wordhash=%', hashed_word)

            #hashed_word = word
            cipher_text = word
            try:
                #result = cursor.fetchall()[0];
                cursor.execute(
                        'update entries set wordhash=%, wordencrypt=%, wordfreq=% where wordhash=%', 
                        (hashed_word, cipher_text, wordcount[word]['freq']))
            except:
                cursor.execute(
                        'insert into entries (wordhash, wordencrypt, wordfreq) values (%s, %s, %s)', 
                        (hashed_word, cipher_text, wordcount[word]['freq']))

            db.commit()
            
        # Render HTML
        self.render("word.html", url=url, results=wordcount)

class RedirectHandler(tornado.web.RequestHandler):
    """Redirects to root URL."""
    def get(self):
        self.redirect("/")

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
    (r"/", HomeHandler),
    (r"/sql", SQLHandler),
    (r"/.*", RedirectHandler),
], **settings)

application = tornado.wsgi.WSGIAdapter(application)
