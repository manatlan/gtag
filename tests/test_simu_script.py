#!/usr/bin/python3 -u
import pytest
from gtag import GTag,Tag,render
from . import GSimu



@pytest.mark.parametrize("webMode", [False,True])
def testInInit(webMode):

    class My(GTag):
        def init(self):
            self("alert(42)")
        def build(self):
            return "Hello"

    def assertRender(x):
        assert "self.bindUpdate" in x
        assert "alert(42)" in x

    cbs=dict(
        eval=assertRender,
        getSessionId= lambda: None, # GID is None
    )

    app=My()
    s=GSimu( app,webMode,cbs)

@pytest.mark.parametrize("webMode", [False,True])
def testInBuild(webMode):

    class My(GTag):
        def build(self):
            self("alert(42)")
            return "Hello"

    def assertRender(x):
        assert "self.bindUpdate" in x
        assert "alert(42)" in x

    cbs=dict(
        eval=assertRender,
        getSessionId= lambda: None, # GID is None
    )
    app=My()
    app.build()
    s=GSimu( app,webMode,cbs)


@pytest.mark.parametrize("webMode", [False,True])
def testInBoth(webMode):

    class My(GTag):
        def init(self):
            self("alert(42)")
        def build(self):
            self("alert(43)")
            return "Hello"

    def assertRender(x):
        assert "self.bindUpdate" in x
        assert "alert(42)" in x
        assert "alert(43)" in x

    cbs=dict(
        eval=assertRender,
        getSessionId= lambda: None, # GID is None
    )

    app=My()
    app.build()
    s=GSimu( app,webMode,cbs)
