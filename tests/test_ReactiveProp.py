from gtag.gtag import GTag, ReactiveProp

def test_ReactiveProp():
    p=dict(a=12,b=42)

    a=ReactiveProp(p,"a")
    assert "<ReactiveProp" in repr(a)
    assert int(a)==12
    assert p["a"]==12
    a.set(42)
    assert p["a"]==42
    assert str(a)=="42"
    a+=1
    assert type(a) is ReactiveProp
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

    a+=b
    assert a == 86

def test_ReactiveProp_bool():
    p=dict(a=True,b=0)

    assert not ReactiveProp(p,"a") == False
    assert not ReactiveProp(p,"b") == True
    assert bool(ReactiveProp(p,"a")) == True
    assert bool(ReactiveProp(p,"b")) == False


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

