#!/usr/bin/env python

from .HTMLElement import HTMLElement
from .text_property import text_property


class HTMLTitleElement(HTMLElement):
    def __init__(self, doc, tag):
        HTMLElement.__init__(self, doc, tag)

    text            = text_property()
