from urllib import FancyURLopener

class wGet(FancyURLopener):
	#version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.19 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.19'
	version = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.26 Safari/535.11'

def wget(url):
	#return urlopen(url).read().replace('\n','')
	m = wGet()
	return m.open(url).read()
	#return urlfetch.fetch(url=url, headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.19 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.19'})

