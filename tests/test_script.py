from gtag import GTag,Tag
import pytest


def test_it():
    class App(GTag):
        def build(self):
            return "hello"
    a=App()
    assert a.script==None


def test_inBuild_with_clone():
    class App(GTag):
        def build(self):
            self.script="api(%s)" % self.id
            return "hello"
    a=App()
    assert a.script=="api(%s)"%a.id    #build() is called at init !
    b=a._clone()
    assert b.script=="api(%s)"%b.id

def test_inInit_with_clone():
    class App(GTag):
        def init(self,v):
            self.v=v
            self.script="api(%s)" % self.id
        def build(self):
            return "hello"
    a=App(1)
    assert a.script=="api(%s)"%a.id    #build() is called at init !
    assert a.v==1

    b=a._clone()
    assert b.script=="api(%s)"%b.id
    assert b.v==1
