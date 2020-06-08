#!/usr/bin/python3 -u
import pytest
from gtag import GTag,Tag,local
from . import GSimu



@pytest.mark.parametrize("webMode", [False,True])
def testSimple(webMode):
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )
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
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )
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
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )
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
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )
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
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )

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
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )
    class My(GTag):
        def build(self):
            return "Hello"
        @local
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
        assert "document.body.innerHTML" in x
        assert "self.bindUpdate(" in x
        assert ",GID,'evt',[1, 10, 30],{})" in x

    cbs=dict(
        render=assertRender,
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
        assert "document.body.innerHTML" in x
        assert "self.bindUpdate(" in x
        assert ",GID,'evt',[1, 10, 30],{})" in x

    cbs=dict(
        render=assertRender,
        getSessionId= lambda: None, # GID is None
    )

    app=My()
    app._call = app.evt(1,c=30)
    s=GSimu( app,webMode,cbs)
