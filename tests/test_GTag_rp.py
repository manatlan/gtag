if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import GTag,Tag,value
from gtag import gtag
import pytest

def test_autocreate_rp():
    class A(GTag):
        def init(self):
            self.v="1"  # RP !
            self._v="1" # not a RP, just a normal STR

    a=A()
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(a.v,str)  # react prop from str!
    assert not isinstance(a._v,gtag.ReactiveProp) # normal prop !
    assert isinstance(a._v,str) # normal prop !
    assert a.v=="1"
    assert a._v=="1"

def test_change_rp_values():
    class A(GTag):
        def init(self):
            self.v=1

    a=A()
    assert isinstance(a.v,gtag.ReactiveProp)
    assert a.v==1

    class B(GTag):
        def init(self,v):
            self.v=v

    b=B(a.v)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert b.v==1

    a.v=2
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==2
    assert b.v==2

    b.v=3
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==3
    assert b.v==3

    a.v+=1
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==4
    assert b.v==4

    a.v-=1
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==3
    assert b.v==3

    a.v*=2
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==6
    assert b.v==6

    a.v/=2
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==3
    assert b.v==3

    a.v//=2
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==1
    assert b.v==1

    a.v=1
    a.v%2
    2%a.v
    a.v%=2

    a.v&2
    2&a.v
    a.v|2
    2|a.v
    a.v^2
    2^a.v
    a.v&=2
    a.v|=2
    a.v^=2

def test_concat_rp_values():
    class A(GTag):
        def init(self):
            self.v="1"

    a=A()
    assert isinstance(a.v,gtag.ReactiveProp)
    assert a.v=="1"

    class B(GTag):
        def init(self,v):
            self.v=v

    b=B(a.v)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert b.v=="1"

    a.v+="x"
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v=="1x"
    assert b.v=="1x"

    a.v=a.v+"y"
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v=="1xy"
    assert b.v=="1xy"

def test_add():
    class A(GTag):
        def init(self,v):
            self.v=v

    a=A(42)
    assert isinstance(a.v,gtag.ReactiveProp)
    assert a.v==42

    b=A(a.v)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert b.v==42

    a.v=a.v+8
    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(b.v,gtag.ReactiveProp)
    assert a.v==50
    assert b.v==50

def test_others():
    class R(GTag):
        def init(self,v):
            self.v=v
    a=R(42)
    b=R(2)

    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(a.v,int)


    assert a.v>b.v
    assert a.v>=b.v
    assert b.v<a.v
    assert b.v<=a.v


    assert a.v + b.v == 44
    assert a.v / b.v == 21
    assert a.v // b.v == 21
    assert a.v + 1 == 43
    assert a.v - 1 == 41
    assert a.v * 2 == 84
    assert a.v / 2 == 21
    assert a.v // 2 == 21

    assert 1 + a.v == 43
    assert 1 - a.v == -41
    assert 2 * a.v == 84
    assert 84 / a.v == 2
    assert 84 // a.v == 2

    assert hash(a.v) == hash(42)

def test_list():
    class R(GTag):
        def init(self,v):
            self.v=v
    a=R( list("abc") )

    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(a.v,list)


    assert len(a.v)==3
    assert "b" in a.v

    for i in a.v:
        assert i in list("abc")

def test_dict():
    class R(GTag):
        def init(self,v):
            self.v=v
    a=R( dict(a=1,b=2) )

    assert isinstance(a.v,gtag.ReactiveProp)
    assert isinstance(a.v,dict)

    assert len(a.v)==2
    assert "a" in a.v
    del a.v["b"]
    assert len(a.v)==1

def test_callable():
    class R(GTag):
        def init(self,v):
            self.v=v
    a=R( lambda x: x )
    assert isinstance(a.v,gtag.ReactiveProp)

    assert a.v(42)==42

def test_gen():
    def g():
        yield 42

    class R(GTag):
        def init(self,v):
            self.v=v
    a=R( g() )
    assert next(a.v)==42


if __name__=="__main__":
    test_GTag()
