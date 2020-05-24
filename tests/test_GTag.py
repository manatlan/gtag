if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import GTag,bind,ReactiveMethod,Tag
from gtag.gui import Div
import pytest

def test_GTag():
    class My(GTag):
        pass
    m=My(None)
    assert m._tag is None
    assert m.build() is None
    # assert m.render() is None
    id=m.id
    assert id
    # assert m._getInstance(id) == m


    with pytest.raises(Exception):
        print(m.bind.unknown)

    with pytest.raises(Exception):
        print(m.bind.unknown())

    with pytest.raises(AssertionError):
        assert str(m)

    assert type(m.update()) is dict


def test_GTag_build():
    class My(GTag):
        def init(self):
            self.v=12
        def build(self):
            return Div("hello",self.bind.v,onclick=self.bind.onclick())
        def onclick(self):
            pass

    m=My()
    o=m.build()
    assert isinstance(o,Tag)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html

    m._tag.js="JS FILE" # possible, because _tag is not dynmacally created (not a @bind bulid)
    assert m._guessCssJs()==(['https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css'], ['JS FILE'])

def test_GTag_render():
    class My(GTag):
        def init(self):
            self.v=12
        @bind
        def build(self):
            return Div("hello",self.bind.v,onclick=self.bind.onclick(42))
        def onclick(self,anArg=None):
            pass

    m=My()
    o=m.build()
    assert isinstance(o,ReactiveMethod)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html

    assert m._guessCssJs()==(['https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css'], [])

def test_GTag_clone():
    class My(GTag):

        def init(self,v):
            self.v=v

        @bind
        def build(self):
            return Div("hello",self.bind.v,onclick=self.bind.onclick(42))
        def onclick(self,anArg=None):
            pass

    m=My(12)
    m.added=42
    o=m.build()
    assert isinstance(o,ReactiveMethod)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html

    assert m._guessCssJs()==(['https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css'], [])

    mm=m._clone()
    assert mm.added==42
    o=m.build()
    assert isinstance(o,ReactiveMethod)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html

    assert m._guessCssJs()==(['https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css'], [])


def test_GTag_clone_with_State():
    class My(GTag):
        def init(self,v):
            self.v=v
        @bind
        def build(self):
            return Div("hello",self.bind.v,onclick=self.bind.onclick(42))
        def onclick(self,anArg=None):
            pass

    m=My(12)
    m.vv=13
    assert m.v==12
    assert m.vv==13

    mm=m._clone() #clone state too
    assert mm.v==12
    assert mm.vv==13

    # m.state.a.set(8)
    # assert m.state.a==8
    # assert mm.state.a==7                    # not same state
    # assert id(mm.state) != id(m.state)      # proof !

    # childM=My( m , 6)
    # assert childM.v==6
    # assert childM.state.a==8
    # assert childM.parent.v==12
    # assert childM.parent.vv==13
    # assert id(childM.state)==id(m.state)

    # childMM=My( mm , 6)
    # assert childMM.v==6
    # assert childMM.state.a==7
    # assert childMM.parent.v==12
    # assert childMM.parent.vv==13
    # assert id(childMM.state)==id(mm.state)




def test_ReactiveMethod():
    class MTag(GTag):
        @bind
        def bm(self,c,nb=2):
            return c*nb

        def m(self,c,nb=2):
            return c*nb

    p=MTag(None)

    assert p.bm("X")() == "XX"
    assert p.bm("O",nb=3)() == "OOO"

    assert p.m("X") == "XX"
    assert p.m("O",nb=3) == "OOO"