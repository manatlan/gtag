#!/usr/bin/python3 -u
from gtag import GTag,Tag,render
from . import GSimu

class Comp(GTag):
    def init(self,value,cpt):
        self.value=value
        self.cpt=cpt
        self.cpt["init"]+=1
    def build(self):
        self.cpt["build"]+=1
        return Tag.div(
            Tag.div( "self=", self.value ),
            Tag.button( "++", onclick=self.bind.clickMe(1) ),
        )
    def clickMe(self,inc):
        self.value+=inc

class App(GTag):
    size=(250,250)
    def init(self):
        self.cpt1=dict(init=0,build=0)
        self.cpt2=dict(init=0,build=0)

        self.v1=0
        self.c2=Comp(0,self.cpt2)

    def build(self):
        return Tag.div(

            "REAL CHILD",
            Comp(self.v1,self.cpt1),"v=",self.v1,
            "<br>",self.cpt1,

            "<hr> INNERCHILD",
            self.c2,"v=",self.c2.value,
            "<br>",self.cpt2,
        )



js=dict(
    eval=lambda x:x,
    getSessionId= lambda: None, # GID is None
)


import pytest
@pytest.mark.parametrize("webMode", [False,True])
def testClickChild(webMode):

    s=GSimu( App(),webMode ,js)

    s.callEvent( s.childs[0].id, "clickMe",1)
    s.callEvent( s.childs[0].id, "clickMe",1)
    s.callEvent( s.childs[0].id, "clickMe",1)

    assert s.main.v1==3
    assert s.main.c2.value==0

    assert s.childs[0].value==3
    assert s.ichilds[0].value==0

    assert s.main.cpt1=={'init': 4, 'build': 4}
    assert s.main.cpt2=={'init': 1, 'build': 4}

    try: # change clickMe() to render local only
        Comp.clickMe.capacities=["local"]

        s=GSimu( App(),webMode ,js)

        s.callEvent( s.childs[0].id, "clickMe",1)
        s.callEvent( s.childs[0].id, "clickMe",1)
        s.callEvent( s.childs[0].id, "clickMe",1)

        assert s.main.v1==3
        assert s.main.c2.value==0

        assert s.childs[0].value==3
        assert s.ichilds[0].value==0

        assert s.main.cpt1=={'init': 1, 'build': 4}
        assert s.main.cpt2=={'init': 1, 'build': 1}

    finally:
        Comp.clickMe.capacities=[]

@pytest.mark.parametrize("webMode", [False,True])
def testClickInnerChild(webMode):
    s=GSimu( App(), webMode ,js )

    s.callEvent( s.ichilds[0].id, "clickMe",1)
    s.callEvent( s.ichilds[0].id, "clickMe",1)
    s.callEvent( s.ichilds[0].id, "clickMe",1)

    assert s.main.v1==0
    assert s.main.c2.value==3

    assert s.childs[0].value==0
    assert s.ichilds[0].value==3

    assert s.main.cpt1=={'init': 4, 'build': 4}
    assert s.main.cpt2=={'init': 1, 'build': 4}

    try: # change clickMe() to render local only
        Comp.clickMe.capacities=["local"]

        s=GSimu( App(),webMode ,js)

        s.callEvent( s.childs[0].id, "clickMe",1)
        s.callEvent( s.childs[0].id, "clickMe",1)
        s.callEvent( s.childs[0].id, "clickMe",1)

        assert s.main.v1==3
        assert s.main.c2.value==0

        assert s.childs[0].value==3
        assert s.ichilds[0].value==0

        assert s.main.cpt1=={'init': 1, 'build': 4}
        assert s.main.cpt2=={'init': 1, 'build': 1}

    finally:
        Comp.clickMe.capacities=[]

@pytest.mark.parametrize("webMode", [False,True])
def testBaseApp(webMode):

    a=App()
    assert a.cpt1=={'init': 0, 'build': 0}
    assert a.cpt2=={'init': 1, 'build': 0}
    s=GSimu( a,webMode,js)
    a.build()
    assert a.cpt1=={'init': 1, 'build': 0}
    assert a.cpt2=={'init': 2, 'build': 0}

    try: # change clickMe() to render local only
        Comp.clickMe.capacities=["local"]

        a=App()
        assert a.cpt1=={'init': 0, 'build': 0}
        assert a.cpt2=={'init': 1, 'build': 0}
        s=GSimu( a,webMode,js)
        a.build()
        assert a.cpt1=={'init': 1, 'build': 0}
        assert a.cpt2=={'init': 2, 'build': 0}

    finally:
        Comp.clickMe.capacities=[]
