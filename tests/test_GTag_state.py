if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import State,GTag,bind
from gtag.gui import Div,Button


class MyState(State):
    def inc(self):                      # not used
        self.a.set(self.a.get()+1)

class ShareState(GTag):
    def build(self):
        return Div( "hello",
            self.state.a,
            self.parent.v
        )

class Page2(GTag):
    def __init__(self,s):
        self.v=42
        self.state=s        # <- self.state will be shared will all gtag (kind of mixins)
        super().__init__(None)

    def build(self):
        return Div(
            ShareState(self) ,
        )


def test_gtag_inherit_state():
    app=Page2( MyState(a=12) )
    assert ">hello 12 42<" in str(app)

if __name__=="__main__":
    test_gtag_inherit_state()