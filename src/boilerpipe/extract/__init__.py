import jpype
import urllib2
import socket
import charade
import threading
import re

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
    - ArticleSentencesExtractor                      file='/home/mj/t20150528_653893.htm'

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
            request     = urllib2.Request(kwargs['url'], headers=self.headers)
            connection  = urllib2.urlopen(request)
            self.data   = connection.read()
            encoding    = connection.headers['content-type'].lower().split('charset=')[-1]
            if encoding.lower() == 'text/html':
                encoding = charade.detect(self.data)['encoding']
            # self.data = unicode(self.data, 'gbk')
            #self.data = self.data.decode(encoding, 'ignore')
            try:
                self.data = unicode(self.data, charade.detect(self.data)['encoding'])
            except UnicodeError:
                encoding = charade.detect(self.data)['encoding']
                self.data = self.data.decode(encoding, 'ignore')
        elif kwargs.get('html'):
            self.data = kwargs['html']
            if not isinstance(self.data, unicode):
                # self.data = unicode(self.data, charade.detect(self.data)['encoding'])
                try:
                    self.data = unicode(self.data, charade.detect(self.data)['encoding'])
                except UnicodeError:
                    encoding = charade.detect(self.data)['encoding']
                    self.data = self.data.decode(encoding, 'ignore')
        ## Extractor(extractor='ArticleExtractor',file='/tmp/a.html')
        elif kwargs.get('file'):
            Path = kwargs['file']
            f = open(Path, 'r')
            self.data = f.read()
            if not isinstance(self.data, unicode):
                try:
                    self.data = unicode(self.data, charade.detect(self.data)['encoding'])
                except UnicodeError:
                    encoding = charade.detect(self.data)['encoding']
                    self.data = self.data.decode(encoding, 'ignore')

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

    def getTitle(self):
        return self.source.getTitle()

    def getHTML(self):
        highlighter = HTMLHighlighter.newExtractingInstance()
        return highlighter.process(self.source, self.data)

    def getDate(self):
        r='(19[7-9][0-9]|20[0-1][0-9])-(0[1-9]|1[0-2])-([1-2][0-9]|0[1-9]|3[0-1]) ([0-1][0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9])'
        return re.search(r,self.data).group()
