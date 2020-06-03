if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))

from gtag import GTag,Tag


class ShareState(GTag):
    def build(self):
        return Tag.div( "hello",
            self.main.a,
            self.parent.v
        )

class Page2(GTag):
    def init(self):
        self.a=12
        self.v=42

    def build(self):
        return Tag.div(
            ShareState() ,
        )

def test_gtag_inherit_state():
    app=Page2( )
    assert ">hello 12 42<" in str(app)

if __name__=="__main__":
    test_gtag_inherit_state()