from gtag import GTag
from gtag.tags import Div,Tag
import pytest

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

    with pytest.raises(AssertionError):
        assert str(m)

    with pytest.raises(AssertionError):
        assert m.update()

def test_GTag_build():
    class My(GTag):

        def __init__(self):
            self.v=12
            super().__init__()
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

def test_GTag_render():
    class My(GTag):

        def __init__(self):
            self.v=12
            super().__init__()
        def render(self):
            return Div("hello",self.bind.v,onclick=self.bind.onclick())
        def onclick(self):
            pass

    m=My()
    o=m.render()
    assert isinstance(o,Tag)
    html=str(m)

    assert 'onclick="self.bindUpdate(' in html
    assert 'id="My_' in html
    assert '>hello 12<' in html
