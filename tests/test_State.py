from gtag import State,ReactiveProp
import pytest

def test_State():

    s=State(a=12)
    assert "<STATE:State" in repr(s)
    assert "<ReactiveProp" in repr(s.a)
    assert int(s.a)==12
    s.a.set(42)
    assert str(s.a)=="42"
    assert type(s.a) is ReactiveProp

    with pytest.raises(Exception):
        s.unknown=12

    with pytest.raises(Exception):
        print(s.unknown)


def test_inherit_state():
    class MyState(State):
        def __init__(self,d):
            super().__init__(**d)

        def change(self,nv):
            self.a.set(nv)

    s=MyState( dict(a=12) )

    assert type(s.a) is ReactiveProp
    assert int(s.a) == 12
    s.change(42)
    assert type(s.a) is ReactiveProp
    assert int(s.a) == 42


