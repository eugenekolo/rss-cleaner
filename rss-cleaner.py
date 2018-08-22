import feedparser
import pprint
import json
from HTMLParser import HTMLParser
from feedgen.feed import FeedGenerator
from xml.sax.saxutils import escape, unescape

class MyHTMLParser(HTMLParser):
    last_link = ''
    real_url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.last_link = attr[1]    
    
    def handle_data(self, data):
        if data == '[link]':
            self.real_url = self.last_link

url = 'https://www.reddit.com/r/netsec/.rss'
feed = feedparser.parse(url)

for article in feed['entries']:
    summary = article['summary']
    
    htmlparser = MyHTMLParser()
    htmlparser.feed(summary)
    link = htmlparser.real_url

    article['link'] = link

fg = FeedGenerator()
fg.icon(feed['feed']['icon'])
fg.id(feed['feed']['id'])
fg.link(feed['feed']['links'])
fg.subtitle(feed['feed']['subtitle'])
fg.title(feed['feed']['title'] + '--FIXED--')
fg.updated(feed['feed']['updated'])

for entry in feed['entries']:
    fe = fg.add_entry()
    fe.author(name=entry['author'])

    fe.content(escape(entry['content'][0]['value']), type=entry['content'][0]['type'])
    fe.id(entry['id'])
    fe.link(entry['links'])
    fe.summary(entry['summary'])
    fe.title(entry['title'])
    fe.description(entry['summary'])

fg.atom_file('reddit-fixed.xml')
