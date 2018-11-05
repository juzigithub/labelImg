#!/usr/bin/env python
# -- coding: UTF-8 --

#
# Copyright (c) 2017 Tzutalin
# Create by TzuTaLin <tzu.ta.lin@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import codecs
import os
import sys
import xml.etree.ElementTree as ET
import re
import json
from textwrap import wrap

try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote

# The script will generate string-[LANG_CODES] and translate it according to the below list
# Short Textual List of Only the Language Codes
#LANG_CODES = ['zh-CN', 'zh-TW']

LANG_CODES = ['zh-CN', 'zh-TW']

'''
LANG_CODES = ['af', 'ach', 'ak', 'ar', 'az', 'be', 'bem', 'bg', 'bh', 'bn', 'br', 'bs', 'ca', 'chr', 'ckb',
'co', 'crs', 'cs', 'cy', 'da', 'de', 'fa', 'fi', 'fo', 'fr', 'fy', 'ga', 'gaa', 'gd', 'gl', 'gn', 'gu',
'ha', 'haw', 'hi', 'hr', 'ht', 'hu', 'hy', 'ia', 'id', 'ig', 'is', 'it', 'iw', 'ja', 'jw', 'ka', 'kg', 'kk',
'km', 'kn', 'ko', 'kri', 'ku', 'ky', 'la', 'lg', 'ln', 'lo', 'loz', 'lt', 'lua', 'lv', 'mfe', 'mg', 'mi', 'mk',
'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'ne', 'nl', 'nn', 'no', 'nso', 'ny', 'nyn', 'oc', 'om', 'or', 'pa', 'pcm',
'pl', 'ps', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sd', 'sh', 'si', 'sk', 'sl', 'sn', 'so', 'sq', 'sr',
'sr-ME', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'tt',
'tum', 'tw', 'ug', 'uk', 'ur', 'uz', 'vi', 'wo', 'xh', 'yi', 'yo', 'zh-CN', 'zh-TW', 'zu']
'''

class Translator:
    def __init__(self, to_lang, from_lang='en'):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, source):
        if self.from_lang == self.to_lang:
            return source
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        res = ''
        for s in self.source_list:
            translate = self._get_translation_from_google(s)
            res = res + (translate if translate is not None else s)
        return res
        #res = ' '.join(self._get_translation_from_google(s) for s in self.source_list)

    def _get_translation_from_google(self, source):
        json5 = self._get_json5_from_google(source)
        data = json.loads(json5)
        translation = data['responseData']['translatedText']
        if not isinstance(translation, bool):
            return translation
        else:
            matches = data['matches']
            for match in matches:
                if not isinstance(match['translation'], bool):
                    next_best_match = match['translation']
                    break
            return next_best_match

    def _get_json5_from_google(self, source):
        escaped_source = quote(source, '')
        headers = {'User-Agent':
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                       (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        api_url = "http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s"
        req = request.Request(url=api_url % (escaped_source, self.from_lang, self.to_lang),
                              headers=headers)

        r = request.urlopen(req)
        return r.read().decode('utf-8')

def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def main():
    global LANG_CODES
    basePairDict = load_properties('strings.properties')
    for lang in LANG_CODES:
        translator = Translator(to_lang=lang)
        outPath = 'strings-' + lang + '.properties'
        output = codecs.open(outPath, 'w', encoding='utf-8')
        for key, value in basePairDict.items():
            translateStr = translator.translate(value)
            output.write("%s=%s\n" % (key, translateStr))
        output.close()

if __name__ == "__main__":
    main()
