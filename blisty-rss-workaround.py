from lxml import etree
import urllib2
import rfc822

class HeadRequest(urllib2.Request):
  def get_method(self):
    return "HEAD"


tree=etree.parse('http://blisty.cz/rss.rb')
tree.getroot().set('version','2.0')

for channel in tree.xpath('//channel[not(language)]'):
  language = etree.Element('language')
  language.text = 'cs'
  language.tail = '\n'
  channel.insert(0,language)

for item in tree.iter('item'):
  try:
    # Update the date element within this item element.
    # Date should be in RFC 822 format, tag should be pubDate
    date = item.find('date')
    date.tag='pubDate'
    # Parse the date into an integer Y,M,D tuple
    date_tag_tuple = tuple( map(int,date.text.split('-')) )
    # Try to find a valid RFC date, including a timestamp, by looking at the article's last-modified HTTP header
    link = item.find('link')
    response = urllib2.urlopen(HeadRequest(item.find('link').text))
    last_modified_tuple = response.headers.getdate('last-modified')
    # Compare the tuples, see if the HTTP header and the original date match
    if date_tag_tuple == last_modified_tuple[:3]:
      #Use the HTTP header as the pubDate
      date.text = response.headers.get('last-modified')
    else:
      # Cannot reliably use the HTTP header -> convert the original date to RFC form
      date_tag_tuple = date_tag_tuple + (12,0,0,0,0,0,0) # noon GMT on the original date
      date.text = rfc822.formatdate(rfc822.mktime_tz(date_tag_tuple))
    
  except:
    pass

print "Content-type: text/plain\n\n"
print etree.tostring(tree,encoding='us-ascii').replace(tree.docinfo.doctype,'',1).strip()
