=================
python-boilerpipe
=================

A python wrapper for Boilerpipe_, an excellent Java library for boilerplate removal and fulltext extraction from HTML pages. 

Configuration
=============

Dependencies:
jpype, chardet

The boilerpipe jar files will get fetched and included automatically when building the package.

Usage
=====

Be sure to have set JAVA_HOME properly since jpype depends on this setting.

The constructor takes a keyword argment ``extractor``, being one of the available boilerpipe extractor types:

- DefaultExtractor
- ArticleExtractor
- ArticleSentencesExtractor
- KeepEverythingExtractor
- KeepEverythingWithMinKWordsExtractor
- LargestContentExtractor
- NumWordsRulesExtractor

If no extractor is passed the DefaultExtractor will be used by default.

::

    from boilerpipe.extract import Extractor
    extractor = Extractor(extractor='ArticleExtractor')

The extractor either accepts HTML or a url as input, either pass ``url`` or ``html`` as a keyword argument::

	extracted_text = extractor.getText(url=your_url)
	
	extracted_html = extractor.getHTML(url=your_url)

.. _Boilerpipe: http://code.google.com/p/boilerpipe/ 