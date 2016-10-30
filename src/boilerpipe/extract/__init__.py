import jpype
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen
import socket
import chardet
import threading

socket.setdefaulttimeout(15)
lock = threading.Lock()

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
    headers   = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, extractor='DefaultExtractor', **kwargs):
        if kwargs.get('url'):
            request     = Request(kwargs['url'], headers=self.headers)
            connection  = urlopen(request)
            self.data   = connection.read()
            encoding    = connection.headers['content-type'].lower().split('charset=')[-1]
            if encoding.lower() == 'text/html':
                encoding = chardet.detect(self.data)['encoding']
            try:
                self.data = unicode(self.data, encoding)
            except NameError:
                self.data = self.data.decode(encoding)
        elif kwargs.get('html'):
            self.data = kwargs['html']
            try:
                if not isinstance(self.data, unicode):
                    self.data = unicode(self.data, chardet.detect(self.data)['encoding'])
            except NameError:
                if not isinstance(self.data, str):
                    self.data = self.data.decode(chardet.detect(self.data)['encoding'])
        else:
            raise Exception('No text or url provided')

        try:
            # make it thread-safe
            if threading.activeCount() > 1:
                if jpype.isThreadAttachedToJVM() == False:
                    jpype.attachThreadToJVM()
            lock.acquire()

            self.extractor = jpype.JClass(
                "de.l3s.boilerpipe.extractors."+extractor).INSTANCE
        finally:
            lock.release()

        reader = StringReader(self.data)
        self.source = BoilerpipeSAXInput(InputSource(reader)).getTextDocument()
        self.extractor.process(self.source)

    def getText(self):
        return self.source.getContent()

    def getHTML(self):
        highlighter = HTMLHighlighter.newExtractingInstance()
        return highlighter.process(self.source, self.data)

    def getImages(self):
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
