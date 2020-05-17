from gtag import GTag
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

