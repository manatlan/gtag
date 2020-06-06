if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import gtag,Tag
from pprint import pprint


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

    assert len(g._childs)==1 #innerchild is no more auto-appended to childs (in constructor) !!!!

def test_convjs():
    assert gtag.convjs([42,b"this.value","he'llo",False,None,3.14,0,True])==['42', "this.value", "'he&#x27;llo'", 'false', 'null', '3.14', '0', 'true']
