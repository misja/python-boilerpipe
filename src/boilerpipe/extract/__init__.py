import urllib2
import socket
import chardet
import threading
from jnius import autoclass

socket.setdefaulttimeout(15)

InputSource        = autoclass('org.xml.sax.InputSource')
StringReader       = autoclass('java.io.StringReader')
HTMLHighlighter    = autoclass('de.l3s.boilerpipe.sax.HTMLHighlighter')
BoilerpipeSAXInput = autoclass('de.l3s.boilerpipe.sax.BoilerpipeSAXInput')

class Extractor(object):
    """
    Extract text. Constructor takes 'extractor' as a keyword argument,
    being one of the boilerpipe extractors:
    - DefaultExtractor
    - ArticleExtractor
    - ArticleSentencesExtractor
    - KeepEverythingExtractor
    - KeepEverythingWithMinKWordsExtractor
    - LargestContentExtractor
    - NumWordsRulesExtractor
    - CanolaExtractor
    """
    extractor = None
    source    = None
    data      = None
    
    def __init__(self, extractor='DefaultExtractor', **kwargs):
        if kwargs.get('url'):
            request   = urllib2.urlopen(kwargs['url'])
            self.data = request.read()
            encoding  = request.headers['content-type'].lower().split('charset=')[-1]
            if encoding.lower() == 'text/html':
                encoding = chardet.detect(self.data)['encoding']
            self.data = unicode(self.data, encoding)
        elif kwargs.get('html'):
            self.data = kwargs['html']
            if not isinstance(self.data, unicode):
                self.data = unicode(self.data, chardet.detect(self.data)['encoding'])
        else:
            raise Exception('No text or url provided')
            
        self.extractor = autoclass(
            "de.l3s.boilerpipe.extractors."+extractor).INSTANCE
    
        reader = StringReader(self.data.encode('utf-8'))
        source = InputSource()
        source.setCharacterStream(reader)
         
        self.source = BoilerpipeSAXInput(source).getTextDocument()
        self.extractor.process(self.source)
    
    def getText(self):
        return self.source.getContent()
    
    def getHTML(self):
        highlighter = HTMLHighlighter.newExtractingInstance()
        return highlighter.process(self.source, self.data)
    
    def getImages(self):
        extractor = autoclass(
            "de.l3s.boilerpipe.sax.ImageExtractor").INSTANCE
        images = extractor.process(self.source, self.data)
        autoclass('java.util.Collections').sort(images)
        images = [
            {
                'src'   : image.getSrc(),
                'width' : image.getWidth(),
                'height': image.getHeight(),
                'alt'   : image.getAlt(),
                'area'  : image.getArea()
            } for image in images
        ]
        return images