Britské listy RSS feed workaround
=================================

This downloads and reformats the RSS feed of the Czech-language blog *Britské listy* (<http://blisty.cz/>)

It roughly works like this:

1. Download the "RSS 1.0" feed from the server and parse it into an XML tree.
2. Add/update some minor cosmetics to make it into a valid RSS 2.0 feed
3. Go through the list of items and correct the dates:
     1. Since the original feed only specifies the date when an item was posted
        (not the time), the script tries to retrieve a valid posting **time** 
        from the HTTP Last-Modified header of the article's link.
     2. If the date part of the HTTP header does not match the original date 
        from the RSS feed, set the date/time to noon GMT on that original date.
4. After processing, output the XML tree in a CGI-compliant way, so that the 
   script can be run on demand from a web server.
