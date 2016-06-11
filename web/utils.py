from google.appengine.ext import db
#from google.appengine.api import urlfetch
from urllib import FancyURLopener

class Data(db.Model):
	item = db.StringProperty()
	#data = db.StringListProperty(required=True)
	data = db.TextProperty()

def put(i, j):
	d = Data()
	d.item = i
	d.data = j
	r = Data.all().filter('item =', d.item)
	db.delete(r)
	d.put()

# Returns the data in an array following this format: [[date],[value],...]
def get(q):
	try: 	
		d = Data.all().filter('item =', q)[0].data
		d = d.split('\n')
		if d[-1] == '': d.pop()
	except: d = []
	return d

def store(i, d, v):
	ld = get(i)
	if ld == []:
		ld.append(d+','+v)
		put(i, '\n'.join(ld))	
	elif ld[-1] != d+','+v: 
		ld.append(d+','+v)
		put(i, '\n'.join(ld))	

class wGet(FancyURLopener):
	#version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.19 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.19'
	version = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.26 Safari/535.11'

def wget(url):
	#return urlopen(url).read().replace('\n','')
	m = wGet()
	return m.open(url).read()
	#return urlfetch.fetch(url=url, headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.19 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.19'})

