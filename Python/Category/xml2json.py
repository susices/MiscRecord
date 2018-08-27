#! /usr/bin/env python
# -*- coding:utf-8 -*-

from xml.parsers.expat import ParserCreate
try:
    import json
except:
    import simplejson as json


class Xml2Json:
    LIST_TAGS = ['COMMANDS']

    def __init__(self, data=None):
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.result = None
        if data:
            self.feed(data)
            self.close()

    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        assert attrs == {}
        assert self._data.strip() == ''
        self._stack.append([tag])
        self._data = ''

    def end(self, tag):
        last_tag = self._stack.pop()
        assert last_tag[0] == tag
        if len(last_tag) == 1:  # leaf
            data = self._data
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_tag[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if type(el) is not list:
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else:  # force into a list
                data = [{k: v} for k, v in last_tag[1:]]
        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self.result = {tag: data}
        self._data = ''

    def data(self, data):
        self._data = data


if __name__ == '__main__':
    xml = """
<student>
    <stid>10213</stid>
    <info>
        <name>name</name>
        <mail>xxx@xxx.com</mail>
        <sex>male</sex>
    </info>
    <course>
        <name>math</name>
        <age>90</age>
    </course>
    <course>
        <name>english</name>
        <age>88</age>
    </course>
</student>
"""
    result = Xml2Json(xml).result
    print(result)
    print("*" * 80)
    print(result['student']['stid'])
    print("*" * 80)
    print(json.dumps(result))
