if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import GTag,bind,Tag
from gtag.gtags import *

import pytest


class MTag(GTag):
    def init(self):
        self.prop1=1
        self.prop2=2

p=MTag()

def test_1():
    b=Button("hello")
    assert str(b).endswith('class="button is-light">hello</button>')
    b=Button("hello",klass="xxx")
    assert str(b).endswith('class="xxx">hello</button>')
    b=Button(p.prop1,klass="xxx")
    assert str(b).endswith('class="xxx">1</button>')
    b=Button(p.bind.prop1,klass="xxx")
    assert str(b).endswith('class="xxx">1</button>')

def test_basics():
    for o in [Button, Input, Section, A, Text, HBox, VBox, Box]:
        assert ">XXX<" in str(o("XXX"))
        assert ">1<" in str(o(p.prop1))
        assert ">1<" in str(o(p.bind.prop1))

def test_Selectors():
    choices=["XXX",1]
    for o in [GRadioButtons,GSelect,GSelectButtons,GTabs]:
        str(o("XXX",choices))
        # assert ">XXX<" in str(o("XXX",choices))
        # assert "> 1 <" in str(o(p.prop1,choices))
        # assert "> 1 <" in str(o(p.bind.prop1,choices))