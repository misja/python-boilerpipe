=================
python-boilerpipe
=================

**I am unable to maintain this project properly anymore, let me know if you'd be interested in taking over**

A python wrapper for Boilerpipe_, an excellent Java library for boilerplate removal and fulltext extraction from HTML pages. 

Configuration
=============

Dependencies:
jpype, charade

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
- CanolaExtractor

If no extractor is passed the DefaultExtractor will be used by default. Additional keyword arguments are either ``html`` for HTML text or ``url``.

::

    from boilerpipe.extract import Extractor
    extractor = Extractor(extractor='ArticleExtractor', url=your_url)

Then, to extract relevant content:

::

	extracted_text = extractor.getText()
	
	extracted_html = extractor.getHTML()

.. _Boilerpipe: http://code.google.com/p/boilerpipe/ 
