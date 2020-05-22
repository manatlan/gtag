from gtag import State,ReactiveProp
import pytest

def test_session():
    class MyState(State):
        def change(self,nv):
            self.a.set(nv)

    s=MyState( a=12 )
    assert s._id==None

    sn="AAA"
    s._initSession(sn)

    sa=State._get(sn)
    assert type(sa.a) is ReactiveProp
    assert int(sa.a) == 12
    sa.change(42)
    assert type(sa.a) is ReactiveProp
    assert int(sa.a) == 42
    assert sa._id==sn

    assert int(s.a) == 12 # original has not changed
    assert int(sa.a) == 42

    assert s._id==None
