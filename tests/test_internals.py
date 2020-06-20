if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag.gtag import GTag
import pytest
from gtag import gtag,Tag
from pprint import pprint
from datetime import datetime


def test_gtag_internals():
    class C(gtag.GTag):
        def build(self):
            return "hello"

    class My(gtag.GTag):
        def init(self):
            self.c=C()
        def build(self):
            return Tag.div( self.c, C())

    g=My()
    assert len(g._ichilds)==1
    d= g._getChilds()
    assert len(d)==3
    assert g.id in d
    assert g.c.id in d

    assert isinstance(g.main.id,str)
    assert g.main.id == g.id
    assert g.main.main.main.id == g.id
    assert g.main.parent is None

    assert g._tree().count("\n") ==2
    #SOMETHING LIKE:
    #       main
    #           child (inner)
    #           child

    assert len(g._childs)==1

    #########################################################
    g._rebuild()
    assert g._ichilds==[g.c] #object created in self container
    d= g._getChilds()
    assert len(d)==3
    assert g.id in d
    assert g.c.id in d

    assert g._tree().count("\n") ==2

    assert len(g._childs)==1

def test_jjs():
    a=["A",b"this.value",False,None,42]
    k=dict(p=12,d=datetime(2020,12,12,1,0,0),c=b"alert(42)")
    assert gtag.jjs(a)=='["A", this.value, false, null, 42]'
    assert gtag.jjs(k)=='{"p": 12, "d": "2020-12-12T01:00:00Z", "c": alert(42)}'



