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
    
    def __init__(self, extractor='DefaultExtractor'):
        self.extractor = jpype.JClass(
            "de.l3s.boilerpipe.extractors."+extractor).getInstance()

    def _source(self, **kwargs):
        if kwargs.get('url'):
            request  = urllib2.urlopen(kwargs['url'])
            data     = request.read()
            encoding = request.headers['content-type'].split('charset=')[-1]
            if encoding.lower() == 'text/html':
                encoding = chardet.detect(data)['encoding']
            data = unicode(data, encoding)
        elif kwargs.get('html'):
            data = kwargs['html']
            if isinstance(data, basestring):
                data = unicode(data, chardet.detect(data)['encoding'])
        else:
            raise Exception('No text or url provided')

        reader = StringReader(data)
        source = BoilerpipeSAXInput(InputSource(reader)).getTextDocument()

        return (source, data)
    
    def getText(self, **kwargs):
        source = self._source(**kwargs)[0]
        self.extractor.process(source)
        return source.getContent()
    
    def getHTML(self, **kwargs):
        source = self._source(**kwargs)
        self.extractor.process(source[0])
        highlighter = HTMLHighlighter.newExtractingInstance()
        return highlighter.process(source[0], source[1])
    
    def getImages(self, **kwargs):
        source = self._source(**kwargs)
        self.extractor.process(source[0])
        extractor = jpype.JClass(
            "de.l3s.boilerpipe.sax.ImageExtractor").INSTANCE
        images = extractor.process(source[0], source[1])
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