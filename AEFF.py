#!/usr/bin/python3 -u
from gtag import GTag,Tag,value


class Star(Tag): # a Star tag for the tests bellow
    tag="Star"
    def __init__(self,v):
        super().__init__("*(%s)"%v)
        self.id="%s" % hex(id(self))[2:]


class Static(GTag):
    """ A full static gtag component without any 'bind' """
    def init(self,n):
        self.n=n


    def stars(self):
        return [Star(i) for i in range( int(self.n) )]

    def build(self):
        return Tag.text(self.n, *self.stars())

class StaticBinded(GTag):
    """ A gtag component with its property bind'ed ! """
    def init(self,n):
        self.n=n


    def stars(self):
        return [Star(i) for i in range(int(self.n))]

    def build(self):
        return Tag.text(self.n, *self.stars())


StaticBinded(2).run()