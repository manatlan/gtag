if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import GTag,bind,Tag
from gtag.gtag import ReactiveMethod,CSS,JS
import pytest

def test_GTag():
    class My(GTag):
        pass
    m=My()
    assert m.parent is None
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
        css="x"
        js="x"
        def init(self):
            self.v=12
        def build(self):
            return Tag.div("hello",self.bind.v,onclick=self.bind.onclick())
        def onclick(self):
            pass

    m=My()
    o=m.build()
    assert isinstance(o,Tag)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html

    hh=m._guessHeaders()
    assert any( [isinstance(i,CSS) for i in hh])
    assert any( [isinstance(i,JS) for i in hh])

def test_GTag_render():
    class My(GTag):
        def init(self):
            self.v=12
        @bind
        def build(self):
            return Tag.div("hello",self.bind.v,onclick=self.bind.onclick(42))
        def onclick(self,anArg=None):
            pass

    m=My()
    o=m.build()
    assert isinstance(o,ReactiveMethod)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html

    hh=m._guessHeaders()
    assert any( [isinstance(i,CSS) for i in hh])


def test_GTag_clone():
    class My(GTag):

        def init(self,v):
            self.v=v

        @bind
        def build(self):
            return Tag.div("hello",self.bind.v,onclick=self.bind.onclick(42))
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

    hh=m._guessHeaders()
    assert any( [isinstance(i,CSS) for i in hh])

    mm=m._clone()
    assert mm.added==42
    o=m.build()
    assert isinstance(o,ReactiveMethod)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html

    hh=m._guessHeaders()
    assert any( [isinstance(i,CSS) for i in hh])


def test_GTag_clone_with_State():
    class My(GTag):
        def init(self,v):
            self.v=v
        @bind
        def build(self):
            return Tag.div("hello",self.bind.v,onclick=self.bind.onclick(42))
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

    p=MTag()

    assert p.bm("X")() == "XX"
    assert p.bm("O",nb=3)() == "OOO"

    assert p.m("X") == "XX"
    assert p.m("O",nb=3) == "OOO"


def test_GTag_with_childs():
    class C(GTag):
        def build(self):
            return Tag.div("hello")

    class MTag(GTag):
        def init(self):
            self.prop=1
        def build(self):
            self.child=C()
            return Tag.div( self.child )
        def test(self):
            return 1


    p=MTag()
    assert p.parent is None
    assert repr(p.main) == repr(p)
    assert repr(p.child.parent) == repr(p)
    assert repr(p.child.main) == repr(p)

    with pytest.raises(Exception):
        print(p.child.parent.unknown())
    with pytest.raises(Exception):
        print(p.child.parent.unknown)
    with pytest.raises(Exception):
        print(p.child.main.unknown())
    with pytest.raises(Exception):
        print(p.child.main.unknown)

    assert p.child.main.prop == 1
    assert p.child.main.test() == 1
    assert p.child.parent.prop == 1
    assert p.child.parent.test() == 1

    assert p._getChild( p.child.id ) is p.child


def test_GTagDyn_with_childs():
    class C(GTag):
        def build(self):
            return Tag.div("hello")

    class MTag(GTag):
        def init(self):
            self.prop=1
        @bind
        def build(self):
            self.child=C()
            return Tag.div( self.child )
        def test(self):
            return 1


    p=MTag()
    assert p.parent is None
    assert repr(p.main) == repr(p)
    str(p) #<-- force to render
    assert repr(p.child.parent) == repr(p)
    assert repr(p.child.main) == repr(p)

    with pytest.raises(Exception):
        print(p.child.parent.unknown())
    with pytest.raises(Exception):
        print(p.child.parent.unknown)
    with pytest.raises(Exception):
        print(p.child.main.unknown())
    with pytest.raises(Exception):
        print(p.child.main.unknown)

    assert p.child.main.prop == 1
    assert p.child.main.test() == 1
    assert p.child.parent.prop == 1
    assert p.child.parent.test() == 1

    assert p._getChild( p.child.id ) is p.child

def test_ReactiveProp():
    class MTag(GTag):
        def init(self):
            self.prop1=1
            self.prop2=2

    p=MTag()
    assert p.prop1 == 1
    assert p.prop2 == 2
    assert p.bind.prop1 == 1
    assert p.bind.prop2 == 2

    p.bind.prop2.set( p.bind.prop1.get() )
    assert p.prop2 == 1

