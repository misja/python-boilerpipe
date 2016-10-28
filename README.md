# python-boilerpipe


A python wrapper for [Boilerpipe](http://code.google.com/p/boilerpipe/), an excellent Java library for boilerplate removal and fulltext extraction from HTML pages.

## Configuration


Dependencies:

 * jpype
 * chardet

The boilerpipe jar files will get fetched and included automatically when building the package.

## Installation


Fedora

    sudo dnf install -y python2-jpype


PIP

    sudo pip install JPype
    sudo pip install chardet
    sudo python setup.py install


## Usage


Be sure to have set `JAVA_HOME` properly since `jpype` depends on this setting.

The constructor takes a keyword argment `extractor`, being one of the available boilerpipe extractor types:

 - DefaultExtractor
 - ArticleExtractor
 - ArticleSentencesExtractor
 - KeepEverythingExtractor
 - KeepEverythingWithMinKWordsExtractor
 - LargestContentExtractor
 - NumWordsRulesExtractor
 - CanolaExtractor

If no extractor is passed the DefaultExtractor will be used by default. Additional keyword arguments are either `html` for HTML text or `url`.

    from boilerpipe.extract import Extractor
    extractor = Extractor(extractor='ArticleExtractor', url=your_url)

Then, to extract relevant content:

    extracted_text = extractor.getText()

    extracted_html = extractor.getHTML()

