#!/usr/bin/python3 -u
import pytest
from gtag import GTag,Tag,render
from . import GSimu

def myexec(x):
    return {}
cbs=dict(
    execute=myexec,
    getSessionId= lambda: None, # GID is None
)



@pytest.mark.parametrize("webMode", [False,True])
def testSimple(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        def evt(self,p):
            self.r=p

    s=GSimu( My(),webMode ,cbs)

    s.callEvent( s.main.id, "evt",1)
    assert s.main.r==1


@pytest.mark.parametrize("webMode", [False,True])
def testSimpleBad(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        def evt(self,p):
            return "yyy" # wtf ?!

    s=GSimu( My(),webMode ,cbs)
    with pytest.raises(Exception):
        s.callEvent( s.main.id, "evt",1)

@pytest.mark.parametrize("webMode", [False,True])
def testSimpleBadAsync(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        async def evt(self,p):
            return "yyy" # wtf ?!

    s=GSimu( My(),webMode ,cbs)
    with pytest.raises(Exception):
        s.callEvent( s.main.id, "evt",1)

@pytest.mark.parametrize("webMode", [False,True])
def testSimpleBadAsyncGen(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        async def evt(self,p):
            yield "yyy" # wtf ?!

    s=GSimu( My(),webMode ,cbs)
    with pytest.raises(Exception):
        s.callEvent( s.main.id, "evt",1)


@pytest.mark.parametrize("webMode", [False,True])
def testSimple2(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        async def evt(self,p):
            self.r=p

    s=GSimu( My(),webMode , cbs)
    s.callEvent( s.main.id, "evt",1)
    assert s.main.r==1

@pytest.mark.parametrize("webMode", [False,True])
def testTheComplex(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        @render.local
        async def evt(self,a,b=10,c=20):
            print("render")
            yield
            print("render")
            self.r=a+b+c

    s=GSimu( My(),webMode,cbs )
    s.callEvent( s.main.id, "evt",1,c=30)
    assert s.main.r==41


@pytest.mark.parametrize("webMode", [False,True])
def testStartAsyncGen(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        async def evt(self,a,b=10,c=20):
            print("render")
            yield
            print("render")
            self.r=a+b+c

    def assertRender(x):
        assert "self.bindUpdate(" in x
        assert ',GID,\'_start\',[],{},{})' in x

        return {}

    cbs=dict(
        execute=assertRender,
        getSessionId= lambda: None, # GID is None
    )

    app=My()
    app._call = app.evt(1,c=30)
    s=GSimu( app,webMode,cbs)

@pytest.mark.parametrize("webMode", [False,True])
def testStartAsync(webMode):

    class My(GTag):
        def build(self):
            return "Hello"
        async def evt(self,a,b=10,c=20):
            self.r=a+b+c

    def assertRender(x):
        assert "self.bindUpdate(" in x
        assert ',GID,\'_start\',[],{},{})' in x
        return {}

    cbs=dict(
        execute=assertRender,
        getSessionId= lambda: None, # GID is None
    )

    app=My()
    app._call = app.evt(1,c=30)
    s=GSimu( app,webMode,cbs)
