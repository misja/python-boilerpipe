import jpype
import urllib2
import socket
import chardet

socket.setdefaulttimeout(15)

InputSource        = jpype.JClass('org.xml.sax.InputSource')
StringReader       = jpype.JClass('java.io.StringReader')
HTMLHighlighter    = jpype.JClass('de.l3s.boilerpipe.sax.HTMLHighlighter')
BoilerpipeSAXInput = jpype.JClass('de.l3s.boilerpipe.sax.BoilerpipeSAXInput')

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
        self._threadSafe()
        self.extractor = jpype.JClass(
            "de.l3s.boilerpipe.extractors."+extractor).INSTANCE
        if kwargs.get('url'):
            request   = urllib2.urlopen(kwargs['url'])
            self.data = request.read()
            encoding  = request.headers['content-type'].split('charset=')[-1]
            if encoding.lower() == 'text/html':
                encoding = chardet.detect(self.data)['encoding']
            self.data = unicode(self.data, encoding)
        elif kwargs.get('html'):
            self.data = kwargs['html']
            if not isinstance(self.data, unicode):
                self.data = unicode(self.data, chardet.detect(self.data)['encoding'])
        else:
            raise Exception('No text or url provided')

        reader = StringReader(self.data)
        self.source = BoilerpipeSAXInput(InputSource(reader)).getTextDocument()
        self.extractor.process(self.source)
    
    def _threadSafe(self):
        if jpype.isThreadAttachedToJVM() == False:
            jpype.attachThreadToJVM()

    def getText(self):
        self._threadSafe()
        return self.source.getContent()
    
    def getHTML(self):
        self._threadSafe()
        highlighter = HTMLHighlighter.newExtractingInstance()
        return highlighter.process(self.source, self.data)
    
    def getImages(self):
        self._threadSafe()
        extractor = jpype.JClass(
            "de.l3s.boilerpipe.sax.ImageExtractor").INSTANCE
        images = extractor.process(self.source, self.data)
        jpype.java.util.Collections.sort(images)
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