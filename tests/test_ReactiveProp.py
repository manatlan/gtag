from gtag.gtag import GTag, ReactiveProp,value


def test_SIMPLE():
    p={}

    a=ReactiveProp(p,"a",12)
    assert "<ReactiveProp" in repr(a)
    assert int(a)==12
    assert p["a"]==12
    p["a"]=42
    assert int(a)==42

def test_ReactiveProp():
    p=dict(a=12,b=42)

    a=ReactiveProp(p,"a")
    assert "<ReactiveProp" in repr(a)
    assert int(a)==12
    assert p["a"]==12
    a.setValue(42)
    assert p["a"]==42
    assert str(a)=="42"
    a+=1
    assert type(a) is int
    a+=1
    assert a == 44

    b=ReactiveProp(p,"b")
    assert a>b
    assert a>0
    assert a>=b
    assert a>=0
    assert b<=a
    assert b<a
    assert b<100
    assert not a==b
    assert a!=b

    b+=a
    assert b == 86
    assert type(b) is int

def test_ReactiveProp_bool():
    p=dict(a=True,b=0)

    assert not ReactiveProp(p,"a") == False
    assert not ReactiveProp(p,"b") == True
    assert bool(ReactiveProp(p,"a")) == True
    assert bool(ReactiveProp(p,"b")) == False

def test_ReactiveProp_object():
    p=dict(a="hello")

    pp=ReactiveProp(p,"a")
    assert pp.upper() == "HELLO"
    assert pp == "hello"
    assert p["a"]=="hello"
    pp.setValue( pp.upper() )
    assert pp=="HELLO"
    assert p["a"]=="HELLO"


def test_ReactiveProp_myobject():
    class O:
        def __init__(self):
            self.toto="hello"
        def test(self):
            return True

    p=dict( a = O() )

    pp=ReactiveProp(p,"a")
    assert pp.toto == "hello"
    p["a"].toto = "yala"
    assert pp.toto == "yala"
    assert pp.test()
    pp.toto="tolo"
    assert p["a"].toto == "tolo"


def test_WARNING():
    class Pojo: pass
    p=Pojo()
    p.a=42

    a=ReactiveProp(p.__dict__,"a")

    assert str(a) == "42"
    assert "-%s-" % a == "-42-"

    p.a=43

    def tt():
        assert str(a) == "43"
        assert "-%s-" % a == "-43-"

def test_GtagProxy_reactiveProp():
    class Pojo: pass
    p=Pojo()
    p.a=42

    class My(GTag):
        def init(self):
            self.v=ReactiveProp(p.__dict__,"a")

    assert isinstance(My().v,ReactiveProp)
    assert My().v==42
    assert isinstance(My().main.v,ReactiveProp)
    assert My().main.v==42

