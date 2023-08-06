tag-text-extractor
==========

Позволяет вытащить из html теги 
'a', 'h2h6', 'text', 'title', 'metadescription', 'beis', 'h1', 'body'
где для каждого тегоа будут получены кол-во слов в нем и список текстов


```
from tag_text_extractor.tag_text_extractor import extract_tag_texts
data = extract_tag_texts("<html><body>...</body></html>")

data.keys()

['a', 'h2h6', 'text', 'title', 'metadescription', 'beis', 'h1', 'body']

data['h2h6']

{
    'texts': [
        u'Account Options', 
        u'Search Options', 
        u'\u0420\u0435\u043a\u043b\u0430\u043c\u0430',
        u'\u0420\u0435\u043a\u043b\u0430\u043c\u0430'
    ],
    'word_count': 6
}

```
