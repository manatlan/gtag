from gtag import State,ReactiveProp
import pytest

def test_State():

    s=State(a=12,b=42)
    assert "<ReactiveProp" in repr(s.a)
    assert int(s.a)==12
    s.a.set(42)
    assert str(s.a)=="42"
    s.a+=1
    assert type(s.a) is ReactiveProp
    s.a+=1
    assert s.a == 44

    # with pytest.raises(AssertionError):
    #     s.ds=12

