if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import gtag,Tag
from pprint import pprint
from datetime import datetime

def test_CSS():
    assert str(gtag.CSS("body {background:yellow}"))=="""<style type="text/css">body {background:yellow}</style>"""
    assert str(gtag.CSS("http:/yo.css"))=="""<link type="text/css" rel="stylesheet" href="http:/yo.css"></link>"""

def test_JS():
    assert str(gtag.JS("alert(42)"))=="""<script type="text/javascript">alert(42)</script>"""
    assert str(gtag.JS("http:/yo.js"))=="""<script type="text/javascript" src="http:/yo.js"></script>"""

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
    assert g.innerChilds==[g.c] #object created in self container
    d= g._getChilds()
    assert len(d)==3
    assert g.id in d
    assert g.c.id in d

    #TODO: do something here (the inner shouldn't be added to child ... no ?)
    assert g._tree().count("\n") ==2
    #SOMETHING LIKE:
    #       main
    #           child (inner)
    #           child

    assert len(g._childs)==2

    #########################################################
    g._rebuild()
    assert g.innerChilds==[g.c] #object created in self container
    d= g._getChilds()
    assert len(d)==3
    assert g.id in d
    assert g.c.id in d

    assert g._tree().count("\n") ==2

    #TODO: do something here (will be the default ... I guess)
    assert len(g._childs)==1 #innerchild is no more auto-appended to childs (in constructor) !!!!

def test_jjs():
    a=["A",b"this.value",False,None,42]
    k=dict(p=12,d=datetime(2020,12,12,1,0,0),c=b"alert(42)")
    assert gtag.jjs(a)=='["A", this.value, false, null, 42]'
    assert gtag.jjs(k)=='{"p": 12, "d": "2020-12-12T01:00:00Z", "c": alert(42)}'



