if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))


from gtag import GTag,Tag,render
import pytest
from . import GSimu

def test_redraw_global():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.bind.v)

        def build(self):
            return Tag.div( self.c, self.bind.v )


    def assertRender(x):
        assert 'document.body.innerHTML=`<div id="A"><div id="C">0</div> 0</div>`' in x

    cbs=dict(
        render=assertRender,
        getSessionId= lambda: None, # GID is None
    )
    app=A(0)
    s=GSimu( app,False,cbs)
    x=s.callEvent("C","evt")
    assert x["script"]=="""document.querySelector("#A").outerHTML=`<div id="A"><div id="C">1</div> 1</div>`;"""



def test_redraw_local():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        @render.local
        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.bind.v)

        def build(self):
            return Tag.div( self.c, self.bind.v )


    def assertRender(x):
        assert 'document.body.innerHTML=`<div id="A"><div id="C">0</div> 0</div>`' in x

    cbs=dict(
        render=assertRender,
        getSessionId= lambda: None, # GID is None
    )

    app=A(0)
    s=GSimu( app,False,cbs)
    x=s.callEvent("C","evt")
    assert x["script"]=="""document.querySelector("#C").outerHTML=`<div id="C">1</div>`;"""

def test_redraw_none(): # STUPID TEST
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        @render.no
        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.bind.v)

        def build(self):
            return Tag.div( self.c, self.bind.v )


    def assertRender(x):
        assert 'document.body.innerHTML=`<div id="A"><div id="C">0</div> 0</div>`' in x

    cbs=dict(
        render=assertRender,
        getSessionId= lambda: None, # GID is None
    )
    app=A(0)
    s=GSimu( app,False,cbs)
    x=s.callEvent("C","evt")
    assert x is None


def test_redraw_parent():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        @render.parent
        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.bind.v)

        def build(self):
            return Tag.div( self.c, self.bind.v )


    def assertRender(x):
        assert 'document.body.innerHTML=`<div id="A"><div id="C">0</div> 0</div>`' in x

    cbs=dict(
        render=assertRender,
        getSessionId= lambda: None, # GID is None
    )

    app=A(0)
    s=GSimu( app,False,cbs)
    x=s.callEvent("C","evt")
    assert x["script"]=="""document.querySelector("#A").outerHTML=`<div id="A"><div id="C">1</div> 1</div>`;"""
