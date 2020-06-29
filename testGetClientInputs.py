#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

from gtag import *


class A(GTag):
    size=(200,200)

    def init(self,v=0,width=b"window.innerWidth"):
        self.c=v
        self.width=width    # here 'width' is b"window.innerWidth" !!!! (not valued!)

    def build(self):
        o=Tag.div( self.width )
        o.add( Tag.button(self.c,onclick=self.bind.add()) )
        return o

    def add(self):
        self.c+=1

class AA(GTag):
    def init(self):
        self.a=A(12)
    def build(self):
        return self.a

if __name__=="__main__":
    a=AA()
    a.run(log=True)
