#!/usr/bin/python3 -u
from gtag import GTag,Tag,local
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
        self.c2=Comp(0,self.bind.cpt2)

    def build(self):
        return Tag.div(

            "REAL CHILD",
            Comp(self.bind.v1,self.bind.cpt1),"v=",self.v1,
            "<br>",self.cpt1,

            "<hr> INNERCHILD",
            self.c2,"v=",self.c2.value,
            "<br>",self.cpt2,
        )





import pytest
@pytest.mark.parametrize("webMode", [False,True])
def testClickChild(webMode):
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )

    s=GSimu( App(),webMode ,cbs)

    s.callEvent( s.childs[0].id, "clickMe",1)
    s.callEvent( s.childs[0].id, "clickMe",1)
    s.callEvent( s.childs[0].id, "clickMe",1)

    assert s.main.v1==3
    assert s.main.c2.value==0

    assert s.childs[0].value==3
    assert s.innerchilds[0].value==0

    assert s.main.cpt1=={'init': 4, 'build': 4}
    assert s.main.cpt2=={'init': 1, 'build': 5}

@pytest.mark.parametrize("webMode", [False,True])
def testClickInnerChild(webMode):
    cbs=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )

    s=GSimu( App(), webMode ,cbs )

    s.callEvent( s.innerchilds[0].id, "clickMe",1)
    s.callEvent( s.innerchilds[0].id, "clickMe",1)
    s.callEvent( s.innerchilds[0].id, "clickMe",1)

    assert s.main.v1==0
    assert s.main.c2.value==3

    assert s.childs[0].value==0
    assert s.innerchilds[0].value==3

    assert s.main.cpt1=={'init': 4, 'build': 4}
    assert s.main.cpt2=={'init': 1, 'build': 5}

def testBase():
    js=dict(
        render=lambda x:x,
        getSessionId= lambda: None, # GID is None
    )
    a=App()
    assert a.cpt1=={'init': 1, 'build': 1}
    assert a.cpt2=={'init': 1, 'build': 1}
    s=GSimu( a,False,js)
    assert a.cpt1=={'init': 1, 'build': 1}
    assert a.cpt2=={'init': 1, 'build': 2}

