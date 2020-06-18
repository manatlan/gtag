
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

def test_TagWithStrangeContent():
    assert str(Tag(False)) == '<div></div>'
    assert str(Tag(True)) == '<div></div>'
    assert str(Tag(None)) == '<div></div>'
    assert str(Tag("1")) == '<div>1</div>'
    assert str(Tag(1)) == '<div>1</div>'
    assert str(Tag(0)) == '<div>0</div>'


def test_Tag_metaclass():
    s=Tag.form(42,klass="jo",checked=True)
    assert str(s) == '<form checked class="jo">42</form>'
    s.klass="jack"
    assert str(s) == '<form checked class="jack">42</form>'


def test_Tag_metaclass2():
    s=Tag.my_tag(42,klass="jo")
    assert str(s) == '<my-tag class="jo">42</my-tag>'



def test_Tag_change_props():
    t=Tag()
    t.id=1
    assert str(t)=='<div id="1"></div>'
    t.id=None
    assert str(t)=='<div></div>'
    t.cid=1
    assert str(t)=='<div cid="1"></div>'
    t.cid=None
    assert str(t)=='<div></div>'

def test_Tag_add():
    t=Tag()
    t.add( Tag.a("click",klass="a"))
    assert str(t)=='<div><a class="a">click</a></div>'

def test_Tag_repr():
    t=Tag()
    t.add( Tag.a("click"))
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
