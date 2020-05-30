from gtag.gui import A,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox
from gtag import Tag

def test_Tag():
    assert str(Tag()) == '<div></div>'
    assert str(Tag(checked=True)) == '<div checked></div>'
    assert str(Tag(checked=False)) == '<div></div>'
    assert str(Tag("hello")) == '<div>hello</div>'
    assert str(Tag("hello",klass="john doe",value=0)) == '<div value="0" class="john doe">hello</div>'
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
