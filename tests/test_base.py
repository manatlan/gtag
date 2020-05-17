from gtag import GTag,ReactiveProp
from gtag.tags import A,Body,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox
from gtag.tags import Tag

def test_ReactiveProp():
    class Pojo: pass
    p=Pojo()
    p.a=12
    p.b=42

    a=ReactiveProp(p,"a")
    assert int(a)==12
    assert p.__dict__["a"]==12
    a.set(42)
    assert p.__dict__["a"]==42
    assert str(a)=="42"
    assert type(a+1) == ReactiveProp
    assert a+1 == 44

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

    assert a+b == 86

def test_Tag():
    assert str(Tag()) == '<div></div>'
    assert str(Tag("hello")) == '<div>hello</div>'
    assert str(Tag("hello",klass="john doe")) == '<div class="john doe">hello</div>'
    assert str(Tag("hello",data_mining="hell")) == '<div data-mining="hell">hello</div>'
    assert str(Tag("hello",42,klass="john doe")) == '<div class="john doe">hello 42</div>'
    assert str(Tag("hello",onclick='alert("bill & john")')) == '<div onclick="alert(&quot;bill &amp; john&quot;)">hello</div>'

def test_Tag_add():
    t=Tag()
    t.add( A("click"))
    assert str(t)=='<div><a class="a">click</a></div>'

def test_Tag_repr():
    t=Tag()
    t.add( A("click"))
    assert repr(t)=='<Tag>'


def test_Tag_id():
    t=Tag()
    t.id="nope"
    assert str(t) == '<div id="nope"></div>'


def test_Tag_class():
    class Nope(Tag): pass
    assert str(Nope()) == '<div></div>'
    assert str(Nope("hello")) == '<div>hello</div>'
    assert str(Nope("hello", klass='other') ) == '<div class="other">hello</div>'

    class Nope(Tag):
        tag="none"
        klass="nine"
    assert str(Nope()) == '<none class="nine"></none>'
    assert str(Nope("hello")) == '<none class="nine">hello</none>'
    assert str(Nope("hello", klass='other') ) == '<none class="other">hello</none>'

def test_GTag():
    class My(GTag):
        pass
    m=My()
    assert m._tag is None
    assert m.build() is None
    assert m.render() is None
    id=m.id
    assert id
    assert m._getInstance(id) == m

