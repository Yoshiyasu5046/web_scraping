import urllib2
import re
import itertools

def download(url, user_agent = "wswp", num_retries = 2):
	print "Downloading:", url
	headers = {'user-agent': user_agent}
	request = urllib2.Request(url, headers = headers)
	try:
		html = urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		print "Download error:", e.reason
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				# recursively retry 5xx HTTP errors
				return download(url, user_agent, num_retries - 1)
	return html

def crawl_sitemap(url):
	# download the sitemap file
	sitemap = download(url)
	# extract the sitemap links
	links = re.findall("<loc>(.*?)</loc>", sitemap)
	# download each link
	for link in links:
		html = download(link)
		# scrape html here

#print download('http://httpstat.us/500')
#print crawl_sitemap("http://example.webscraping.com/sitemap.xml")

# maximum number of consecutive download errors allowed
max_errors = 5
# current number of consecutive download errors 
num_errors = 0
for page in itertools.count(1):
	url = "http://example.webscraping.com/view/-%d" % (page)
	html = download(url)
	if html is None:
		# received an error trying to download this webpage
		num_errors += 1
		if num_errors == max_errors:
		# reached maximum number of consecutive errors. so exit.
			break 
	else:
		# success - can scrape the result
		pass
